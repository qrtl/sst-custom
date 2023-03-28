# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResOccupation(models.Model):
    _name = "res.occupation"

    name = fields.Char(required=True)
