# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models,fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    is_invoice_issuer = fields.Boolean()

    @api.onchange("partner_id")
    def onchange_invoice_partner_id(self):
        if self.partner_id:
            self.is_invoice_issuer = self.partner_id.is_invoice_issuer
