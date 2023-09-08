# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from datetime import datetime

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_price = fields.Float(track_visibility="onchange")
