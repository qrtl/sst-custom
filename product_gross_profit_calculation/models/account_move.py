# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        moves = super(AccountMove, self)._post(soft=soft)
        for move in self:
            if move.state == "posted" and move.move_type == "out_invoice":
                for line in move.invoice_line_ids:
                    line.product_id.write(
                        {
                            "sale_price_unit": line.price_total / line.quantity
                            if line.quantity
                            else 0.0,
                        }
                    )
        return moves
