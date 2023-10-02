# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def update_stock_move_done_qty(self):
        stock_moves = self.env["stock.move"].search(
            [
                ("product_id", "=", self.product_id.id),
                ("state", "not in", ("done", "draft", "cancel")),
            ],
            order="date",
        )
        stock_quantity = self.quantity
        for stock_move in stock_moves:
            if (
                stock_move.location_dest_id.usage == "customer"
                and stock_quantity
                and stock_move.quantity_done < stock_move.product_uom_qty
            ):
                stock_move.quantity_done = (
                    stock_move.product_uom_qty
                    if stock_quantity > stock_move.product_uom_qty
                    else stock_quantity
                )
                stock_quantity -= stock_move.quantity_done
