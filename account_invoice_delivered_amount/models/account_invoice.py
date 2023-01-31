# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    total_delivered_amount = fields.Monetary(string="Total Delivered Amount", currency_field="currency_id",
        store=True, compute="_compute_delivered_amount")
    total_delivered_amount_signed = fields.Monetary(string='Total Delivered Amount in Company Currency', currency_field='company_currency_id',
        store=True, compute='_compute_delivered_amount')

    @api.depends("invoice_line_ids.is_delivered", "invoice_line_ids.deliverd_amount")
    def _compute_delivered_amount(self):
        for invoice in self:
            invoice.total_delivered_amount = sum(line.deliverd_amount for line in invoice.invoice_line_ids)
            total_delivered_amount_signed = invoice.total_delivered_amount
            if invoice.currency_id and invoice.company_id and invoice.currency_id != invoice.company_id.currency_id:
                currency_id = invoice.currency_id.with_context(date=invoice.date_invoice)
                total_delivered_amount_signed = currency_id.compute(invoice.total_delivered_amount, invoice.company_id.currency_id)
            invoice.total_delivered_amount_signed = total_delivered_amount_signed
