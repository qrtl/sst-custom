# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    in_cart = fields.Boolean(related="product_id.in_cart")
