# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    shop_id = fields.Many2one(
        related="invoice_id.shop_id",
        string="Shop",
        readonly=True,
    )
