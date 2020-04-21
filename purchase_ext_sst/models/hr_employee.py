# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    shop_id = fields.Many2one("stock.warehouse", "Shop")
