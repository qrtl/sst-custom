# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def write(self, vals):
        if vals.get('default_code') and vals['default_code'].isdigit():
            vals['barcode'] = vals['default_code']
        return super(ProductProduct, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        if res.default_code and res.default_code.isdigit():
            res.barcode = res.default_code
        return res
