# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        # This method does not work for line items that include both inclusive and exclusive taxes. 
        # It assumes that the sales order only contains lines with either inclusive or exclusive taxes.
        res = super()._amount_all()
        for order in self:
            amount_tax = amount_total = 0.0
            for line in order.order_line:
                # If exclusive tax is included in the sale.order.line, the original logic will be used.
                if not line.tax_id.price_include:
                    return
                amount_tax += line.price_tax
                amount_total += line.price_total
            order.update({
                'amount_untaxed': amount_total - amount_tax, 
                'amount_total': amount_total,
            })
