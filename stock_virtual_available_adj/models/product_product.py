# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    draft_sale_qty = fields.Float(
        'Sale Quantity (Draft)',
        compute='_compute_sale_quantities',
        help='Total quantity of the product in draft sales order(s)',
    )
    sent_sale_qty = fields.Float(
        'Sale Quantity (Sent)',
        compute='_compute_sale_quantities',
        help='Total quantity of the product in sent sales order(s)',
    )
    website_sale_available_qty = fields.Float(
        'Available Quantity in eCommerce',
        compute='_compute_website_sale_available_qty',
        help='Available quantity of the product in eCommerce, excluding the '
             'quantities in sent and draft sales order as well',
    )

    @api.multi
    def _compute_sale_quantities(self):
        for product in self:
            sale_lines = self.env['sale.order.line'].search(
                [('product_id', '=', product.id),
                 ('state', 'in', ('sent', 'draft'))])
            product.draft_sale_qty = sum(sale_lines.filtered(
                lambda p: p.state == 'draft').mapped('product_uom_qty'))
            product.sent_sale_qty = sum(sale_lines.filtered(
                lambda p: p.state == 'sent').mapped('product_uom_qty'))

    @api.multi
    def _compute_website_sale_available_qty(self):
        for product in self:
            product.website_sale_available_qty = product.virtual_available - \
                                                 product.sent_sale_qty - \
                                                 product.draft_sale_qty
