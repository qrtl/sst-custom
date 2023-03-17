# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DataImportLog(models.Model):
    _inherit = "data.import.log"

    sale_order_ids = fields.One2many(
        "sale.order", "data_import_log_id", string="Related Sale Orders"
    )
