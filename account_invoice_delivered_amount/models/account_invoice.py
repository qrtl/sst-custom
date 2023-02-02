# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    amount_total_delivered = fields.Monetary(
        string="Total Delivered Amount",
        store=True,
        compute="_compute_amount_delivered",
    )
    amount_total_delivered_signed = fields.Monetary(
        string="Total Delivered Amount (+/-)",
        store=True,
        compute="_compute_amount_delivered",
    )
    delivery_done = fields.Boolean(compute="_compute_amount_delivered", store=True)

    @api.depends(
        "invoice_line_ids.is_delivered", "invoice_line_ids.delivered_amount", "type"
    )
    def _compute_amount_delivered(self):
        for invoice in self:
            if invoice.type not in ["out_invoice", "out_refund"]:
                continue
            sign = -1 if invoice.type == "out_refund" else 1
            invoice.amount_total_delivered = sum(
                invoice.invoice_line_ids.mapped("delivered_amount")
            )
            invoice.amount_total_delivered_signed = (
                invoice.amount_total_delivered * sign
            )
            if invoice.amount_total_delivered == invoice.amount_total:
                invoice.delivery_done = True
