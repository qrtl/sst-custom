# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    website_published = fields.Boolean(
        related="product_id.website_published",
        string="Visible in Website",
    )
    list_price = fields.Float(
        related="product_id.product_tmpl_id.list_price", string="Sale Price",
    )
    # To improve search performance by product.
    product_id = fields.Many2one(auto_join=True,)
    default_code = fields.Char(
        related="product_id.default_code",
        string="Barcode",
        store=True,
        readonly=True,
        index=True,
    )
