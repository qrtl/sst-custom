# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MemeberGroup(models.Model):
    _name = "member.group"

    name = fields.Char(
        string="Group Name",
        required=True,
    )
    point_limit = fields.Integer(
        string="Points Limit",
        required=True,
    )
