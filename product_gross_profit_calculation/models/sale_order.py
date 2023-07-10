# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            template = line.product_id.product_tmpl_id
            template.write(
                {
                    "sale_price_unit": line.price_reduce_taxinc,
                    "confirmation_date": self.date_order,
                    "team_id": self.team_id.id,
                }
            )
        return res
