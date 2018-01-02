# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons import decimal_precision as dp

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_price_unit = fields.Monetary(
        string='Sale Price (Actual)',
        digits = dp.get_precision('Product Price'),
        readonly=True,
        store=True,
    )
    gross_profit = fields.Monetary(
        string='Gross Profit',
        digits=dp.get_precision('Product Price'),
        compute='_compute_gross_profit',
        readonly=True,
        store=True,
    )
    confirmation_date = fields.Datetime(
        string='Confirmation Date',
        readonly=True,
    )
    team_id = fields.Many2one(
        'crm.team',
        string='Sales Channel',
        readonly=True,
    )

    @api.depends('sale_price_unit', 'list_price', 'standard_price')
    def _compute_gross_profit(self):
        for pt in self:
            if pt.sales_count:
                pt.gross_profit = pt.sale_price_unit - pt.standard_price
            else:
                pt.gross_profit = pt.list_price - pt.standard_price
