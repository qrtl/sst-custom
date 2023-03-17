# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    picking_policy = fields.Selection(
        [("direct", "As soon as possible"), ("one", "When all products are ready")],
        string="Shipping Policy",
    )
    customer_invoice_journal_id = fields.Many2one(
        "account.journal",
        string="Customer Invoice Journal",
    )
    customer_payment_journal_id = fields.Many2one(
        "account.journal",
        string="Customer Payment Journal",
    )
