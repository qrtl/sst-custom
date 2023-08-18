# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class YahooProductState(models.Model):
    _name = "yahoo.product.state"

    name = fields.Char(string="Status", require=True,)
