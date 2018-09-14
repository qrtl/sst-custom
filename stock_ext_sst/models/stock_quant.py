# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    website_published = fields.Boolean(
        related='product_id.product_tmpl_id.website_published',
        string='Visible in Website',
    )
    yahoo_product_state_id = fields.Many2one(
        related='product_id.product_tmpl_id.yahoo_product_state_id',
        string='Yahoo Product State',
    )
    list_price = fields.Float(
        related='product_id.product_tmpl_id.list_price',
        string='Sale Price',
    )
    product_id = fields.Many2one(
        auto_join=True,
    )

    def update_stock_move_done_qty(self):
        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', self.product_id.id),
            ('state', 'in', ('confirmed', 'waiting'))
        ], order='date')
        for stock_move in stock_moves:
            if stock_move.picking_type_id.default_location_dest_id.usage == \
                    'customer':
                stock_move.quantity_done = stock_move.product_uom_qty if \
                    self.quantity > stock_move.product_uom_qty else \
                    self.quantity
                return
