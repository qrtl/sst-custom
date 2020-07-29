# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class ProductPriceRecord(models.Model):
    _name = "product.price.record"

    string = fields.Char("String Pattern", required=True,)
    product_state_id = fields.Many2one("product.state", "Product State", required=True,)
    price = fields.Float(
        "Price", digits=dp.get_precision("Product Price"), required=True, default=0.0
    )
    public_categ_id = fields.Many2one(
        "product.public.category", "Website Product Category",
    )
