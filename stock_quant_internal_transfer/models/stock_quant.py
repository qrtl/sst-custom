## -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    picking_id = fields.Many2one(
        'stock.picking',
        string='Stock Picking',
    )
