# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _compute_amount(self):
        super()._compute_amount()
        # Use the original logic for exclusive tax cases.
        # We assume that that there is no situation where
        # lines contain tax inclusive and exclusive cases in an invoice at the same time..
        taxes = self.invoice_line_ids.mapped("invoice_line_tax_ids")
        if not taxes or any(not tax.price_include for tax in taxes):
            return
        self.amount_total = sum(line.price_total for line in self.invoice_line_ids)
        self.amount_untaxed = self.amount_total - self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if (
            self.currency_id
            and self.company_id
            and self.currency_id != self.company_id.currency_id
        ):
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(
                self.amount_total, self.company_id.currency_id
            )
            amount_untaxed_signed = currency_id.compute(
                self.amount_untaxed, self.company_id.currency_id
            )
        sign = self.type in ["in_refund", "out_refund"] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign
