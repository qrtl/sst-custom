# -*- coding: utf-8 -*-

from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
