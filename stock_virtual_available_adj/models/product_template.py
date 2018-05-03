# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_sale_available_qty = fields.Float(
        'Available Quantity in eCommerce',
        compute='_compute_website_sale_available_qty',
        help='Available quantity of the product in eCommerce, excluding the '
             'quantities in sent and draft sales order as well',
    )

    @api.multi
    def _compute_website_sale_available_qty(self):
        for pt in self:
            for pp in pt.product_variant_ids:
                pt.website_sale_available_qty += pp.virtual_available - \
                                                 pp.sent_sale_qty - \
                                                 pp.draft_sale_qty
