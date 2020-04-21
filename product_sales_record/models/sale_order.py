# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order_line in self.order_line:
            product = order_line.product_id.product_tmpl_id
            product.write(
                {
                    "sale_price_unit": order_line.price_reduce_taxinc,
                    "confirmation_date": self.confirmation_date,
                    "team_id": self.team_id.id,
                }
            )
        return res
