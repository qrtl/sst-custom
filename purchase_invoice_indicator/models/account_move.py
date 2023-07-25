# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    is_invoice_issuer = fields.Boolean()

    @api.onchange("partner_id")
    def onchange_invoice_partner_id(self):
        if self.partner_id:
            self.is_invoice_issuer = self.partner_id.is_invoice_issuer
