# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_state_id = fields.Many2one("product.state", "Product State")
