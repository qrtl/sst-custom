# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    team_ids = fields.Many2many(
        'crm.team',
        'product_tmpl_team_rel',
        'product_tmpl_id',
        'team_id',
        'Sales Channels',
    )
    manufacturer = fields.Char()
    manufactured_year = fields.Selection(
        [(num, str(num)) for num in reversed(
            range(1900, datetime.now().year+1))],
        'Manufactured Year',
    )
    model = fields.Char()
    product_state_id = fields.Many2one('product.state', 'Product State')
    purchase_category_id = fields.Many2one(
        'purchase.category',
        'Purchase Category',
    )
    evaluated_by_id = fields.Many2one('hr.employee', "Evaluated By")
    purchased_by_id = fields.Many2one('hr.employee', "Purchased By")
    shop_id = fields.Many2one('stock.warehouse', string='Shop Purchased')

    @api.multi
    def open_record(self):
        form_id = self.env.ref('product.product_template_only_form_view')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {},
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        if 'title' in vals:
            query = """
                        SELECT
                            price
                        FROM
                            product_price_record
                        WHERE
                            %s LIKE '%%' || string || '%%'
                    """
            query_param = [vals['title']]
            if 'product_state_id' in vals:
                query += """
                AND
                    product_state_id = %s
                """
                query_param.append(vals['product_state_id'])
            query += """
                ORDER BY CHAR_LENGTH(string) DESC
                LIMIT 1;
            """
            if not 'list_price' in vals or vals['list_price'] == 0:
                self.env.cr.execute(query, query_param)
                result = self.env.cr.fetchone()
                if result:
                    vals['list_price'] = result[0]
        return super(ProductTemplate, self).create(vals)
