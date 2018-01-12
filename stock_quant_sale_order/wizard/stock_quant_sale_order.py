# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
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

    @api.multi
    def action_stock_quant_saleorder(self):
        '''This method create a sale order.'''
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        stock_quant_obj = self.env['stock.quant']
        quant_ids = stock_quant_obj.browse(active_ids)
        source_location = quant_ids[0].location_id
        if any(q.location_id != source_location for q in quant_ids):
            raise UserError(_('Please select quants that are in the same '
                              'Location.'))
        if any(q.sale_order_id for q in quant_ids):
            raise UserError(
                _('Some of the selected quants are already create sale order.')
            )
        if any(
            self .env.user.company_id.id != q.company_id.id for q in quant_ids
        ):
            raise UserError(
                _('You can not create sales order for different company.')
            )
        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        origin_name = ','.join([q.display_name for q in quant_ids])
        order_vals = {
            'partner_id': self.partner_id.id,
            'state': 'draft',
            'origin': origin_name,
        }
        sale_order = sale_order_obj.sudo().create(order_vals)
        sale_order.onchange_partner_id()
#         sale_order.onchange_partner_id_carrier_id()

        for quant in quant_ids:
            quant.sudo().sale_order_id = sale_order.id
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
