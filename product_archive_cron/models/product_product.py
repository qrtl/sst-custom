# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _process_product_archive(self):
        self.env.cr.execute("""
            SELECT
                product_id,
                sum(product_qty) AS purch_qty
            FROM
                purchase_order_line
            WHERE
                state in ('sent', 'draft')
            GROUP BY
                product_id
        """)
        purch_dict = self.env.cr.dictfetchall()

        purch_vals = {}
        for dict in purch_dict:
            purch_vals[dict['product_id']] = dict['purch_qty']

        for prod in self.search(
                [('type', '=', 'product'), ('active', '=', True)]):
            if prod.virtual_available + purch_vals.get(prod.id, 0) + \
                    prod.draft_sale_qty + prod.sent_sale_qty <= 0:
                # if product has reordering rules then deactivate first
                if prod.orderpoint_ids:
                    prod.orderpoint_ids.write({'active': False})
                prod.product_tmpl_id.write({'active': False})
