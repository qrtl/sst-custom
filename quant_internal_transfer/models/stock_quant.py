# -*- coding: utf-8 -*-

from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    picking_id = fields.Many2one(
        'stock.picking',
        string='Stock Picking',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
