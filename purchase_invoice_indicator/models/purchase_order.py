# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models,api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def action_view_invoice(self):
        res = super(PurchaseOrder, self).action_view_invoice()
        if res.get("context"):
            res["context"].update(
                default_is_invoice=self.partner_id.is_invoice_issuer,
            )
        return res
