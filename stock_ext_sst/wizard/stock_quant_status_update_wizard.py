# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockQuantStatusUpdate(models.TransientModel):
    _name = 'stock.quant.status.update.wizard'

    yahoo_product_state_id = fields.Many2one(
        'yahoo.product.state',
        string='Yahoo Product State',
    )

    def action_stock_quant_status_update(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        quants = self.env['stock.quant'].browse(active_ids)
        values = {
            'website_published': self.yahoo_product_state_id.website_published,
            'yahoo_product_state_id': self.yahoo_product_state_id.id
        }
        for quant in quants:
            quant.product_id.product_tmpl_id.sudo().write(values)
            if self.yahoo_product_state_id.id == int(self.env[
                'ir.config_parameter'].sudo().get_param(
                'stock_ext_sst.picking_product_state_id')):
                quant.update_stock_move_done_qty()
