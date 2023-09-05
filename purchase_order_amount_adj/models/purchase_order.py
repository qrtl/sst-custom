# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurcahseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends("order_line.price_total")
    def _amount_all(self):
        # This method does not work for line items that include
        # both inclusive and other taxes.
        # It assumes that the purchase order only contains lines
        # with inclusive taxes.
        super()._amount_all()
        for order in self:
            amount_tax = amount_total = 0.0
            for line in order.order_line:
                # Use the original logic if a tax other than 
                # the inclusive tax is applied to purchase.order.line.
                if any(not tax.price_include for tax in line.taxes_id):
                    return
                amount_tax += line.price_tax
                amount_total += line.price_total
            order.update(
                {
                    "amount_untaxed": amount_total - amount_tax,
                    "amount_total": amount_total,
                }
            )
