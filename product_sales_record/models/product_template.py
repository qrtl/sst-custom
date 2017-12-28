# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons import decimal_precision as dp

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    list_price_record = fields.Monetary(
        string='Sale Price Record',
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

    @api.depends('list_price_record', 'list_price', 'standard_price')
    def _compute_gross_profit(self):
        for product in self:
            if product.standard_price:
                if product.list_price_record and \
                                product.list_price_record != 0:
                    product.gross_profit = product.list_price_record - \
                                           product.standard_price
                elif product.list_price:
                    product.gross_profit = product.list_price - \
                                           product.standard_price
