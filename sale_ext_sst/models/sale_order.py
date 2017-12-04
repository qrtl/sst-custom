# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    phone = fields.Char(
        related='partner_id.phone',
        string='Phone',
    )
    order_item = fields.Many2one(
        'product.product',
        string='Product',
        compute='_get_first_product',
    )

    @api.depends('order_line')
    def _get_first_product(self):
        for order in self:
            for order_line in order:
                order.order_item = order_line.product_id
                break
