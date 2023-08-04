# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals["is_invoice_issuer"] = self.partner_id.is_invoice_issuer
        return invoice_vals
