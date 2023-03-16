# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class YahooProductState(models.Model):
    _name = "yahoo.product.state"

    name = fields.Char(
        string="Status",
        require=True,
    )
