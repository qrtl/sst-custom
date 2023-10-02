# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    sales_channel_id = fields.Many2one(
        related="product_tmpl_id.sales_channel_id", string="Exp. Sales Channel",
    )
