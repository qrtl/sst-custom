# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ErrorLog(models.Model):
    _inherit = "error.log"

    sale_order_ids = fields.One2many(
        "sale.order", "error_log_id", string="Related Sale Orders"
    )
