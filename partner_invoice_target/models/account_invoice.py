# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models,fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    # override vat to add translation
    vat = fields.Char()
    is_invoice_target = fields.Boolean(related="partner_id.is_invoice_target", store=True, readonly=True)
