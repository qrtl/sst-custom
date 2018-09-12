# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Follows the set_delivery_line in the website_sale_delivery
    def _create_order_line(self, product_id):
        # Apply fiscal position
        taxes = product_id.taxes_id.filtered(
            lambda t: t.company_id.id == self.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(
                taxes, product_id, self.partner_id).ids
        # Create the penalty product order line
        values = {
            'order_id': self.id,
            'product_uom_qty': 1,
            'product_uom': product_id.uom_id.id,
            'product_id': product_id.id,
            'price_unit': product_id.list_price,
            'tax_id': [(6, 0, taxes_ids)],
            'is_penalty': True
        }
        if self.order_line:
            values['sequence'] = self.order_line[-1].sequence + 1
        sol = self.env['sale.order.line'].sudo().create(values)
        return sol
