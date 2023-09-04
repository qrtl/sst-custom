# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        res = super()._amount_all()
        for order in self:
            amount_tax = amount_total=0.0
            for line in order.order_line:
                amount_tax += line.price_tax
                amount_total += line.price_total
            order.update({
                'amount_untaxed': amount_total - amount_tax, 
                'amount_total': amount_total,
            })
