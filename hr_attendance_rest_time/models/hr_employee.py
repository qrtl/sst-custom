# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

REST_TIME = [
    ("0", "0"),
    ("15", "15"),
    ("30", "30"),
    ("45", "45"),
    ("60", "60"),
    ("75", "75"),
    ("90", "90"),
]


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    rest_time_standard = fields.Selection(
        REST_TIME, "Standard Rest Time (minutes)", default="0"
    )
