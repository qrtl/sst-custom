# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    imported_order = fields.Boolean(
        "Is Imported",
        readonly=True,
    )
    order_ref = fields.Char(
        "Order Reference",
        readonly=True,
    )
    data_import_log_id = fields.Many2one(
        "data.import.log",
        string="Import Log",
        readonly=True,
    )
    invoiceable = fields.Boolean(
        readonly=True,
        default=True,
    )
