# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QuantSaleOrderWizard(models.TransientModel):
    _name = 'quant.sale.order.wizard'

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
    )
    team_id = fields.Many2one(
        'crm.team',
        string='Sales Channel',
        required=True,
    )

    @api.model
    def default_get(self, fields):
        """Raise to warning in
            - selected quants not in same location.
            - selected quants are already create sale order.
            - selected quants company is not same to user company.
        """
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        active_model = context.get('active_model')
        quant_ids = self.env[active_model].browse(active_ids)
        source_location = quant_ids[0].location_id
        if any(q.location_id != source_location for q in quant_ids):
            raise UserError(_('Please select quants that are in the same '
                              'Location.'))
        if source_location.usage != 'internal':
            raise UserError(_('Please select quants that are in the internal '
                              'location to create the sales order.'))
        order_line_list = self.env['sale.order.line'].search([
            ('state', 'not in', ['done', 'cancel']),
            ('product_id', 'in', [q.product_id.id for q in quant_ids])
        ])
        if order_line_list:
            error_msg = ''
            for order_line in order_line_list:
                error_msg += '\n%s: %s' % (
                    order_line.order_id.name,
                    order_line.product_id.display_name,
                )
            raise UserError(_('There is at least one active sales order '
                              'that uses the product of a selected quant: '
                              '%s') % error_msg)
        if any(self .env.user.company_id.id != q.company_id.id for q in
               quant_ids):
            raise UserError(_('You cannot create sales order from stock '
                              'quants that belongs to other company.'))
        return super(QuantSaleOrderWizard, self).default_get(fields)

    @api.multi
    def action_create_sale_order(self):
        '''This method create a sale order.'''
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        stock_quant_obj = self.env['stock.quant']
        quant_ids = stock_quant_obj.browse(active_ids)
        warehouse_id = self.get_warehouse_id(quant_ids[0].location_id)
        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        order_vals = {
            'partner_id': self.partner_id.id,
            'team_id': self.team_id.id,
            'company_id': self.env.user.company_id.id,
            'state': 'draft',
            'warehouse_id': warehouse_id.id,
        }
        sale_order = sale_order_obj.sudo().create(order_vals)
        sale_order.onchange_partner_id()
        sale_order.user_id = self.env.uid

        for quant in quant_ids:
            line_vals = {
                'product_id': quant.product_id.id,
                'product_uom_qty': quant.quantity,
                'order_id': sale_order.id,
            }
            sale_order_line_obj.sudo().create(line_vals)

        action = self.env.ref('sale.action_quotations')
        action_vals = action.read()[0]
        action_vals['domain'] = str([('id', '=', sale_order.id)])
        return action_vals

    def get_warehouse_id(self, location_id):
        stock_warehouse_obj = self.env['stock.warehouse']

        location_list = []
        location = location_id
        while location:
            location_list.append(location.id)
            location = location.location_id

        warehouse_id = stock_warehouse_obj.search(
            [('view_location_id', 'in', location_list),
             ('company_id', '=', self.env.user.company_id.id)],
            limit=1
        )
        if not warehouse_id:
            raise UserError(_('The stock location does not belong to any '
                              'warehouse.'))
        return warehouse_id
