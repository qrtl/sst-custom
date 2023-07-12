# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrderCancel(models.TransientModel):
    _name = "purchase.order.cancel"

    @api.model
    def _cancel_purchase_order(self, orders):
        return orders.button_cancel()

    def action_cancel_purchase_order(self):
        active_ids = self._context.get("active_ids", [])
        active_model = self._context.get("active_model", "purchase.order")
        orders = self.env[active_model].browse(active_ids)
        self._cancel_purchase_order(orders)
