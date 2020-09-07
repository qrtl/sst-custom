# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResIdentificationType(models.Model):
    _name = "res.identification.type"

    name = fields.Char(required=True)
