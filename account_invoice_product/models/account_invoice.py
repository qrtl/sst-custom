# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    product_id = fields.Many2one(
        "product.product", related="invoice_line_ids.product_id", string="Product"
    )
