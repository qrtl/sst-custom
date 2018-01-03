# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    barcode = fields.Char(
        compute="_get_barcode",
        store=True,
    )

    @api.depends('default_code')
    def _get_barcode(self):
        for pp in self:
            pp.barcode = pp.default_code
