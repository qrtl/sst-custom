# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    title = fields.Char(
        string='Title',
    )
    product_category = fields.Char(
        string='Product Category',
    )
    product_condition_comment = fields.Text(
        string='Product Condition Comment',
    )
    accessories = fields.Char(
        string='Accessories',
    )
    remark = fields.Text(
        string='Remark',
    )
    staff_in_charge = fields.Many2one(
        'hr.employee',
        string='Staff in charge',
    )
    auction_start_price = fields.Monetary(
        string='Auction Starting Price',
    )
    auction_buyout_price = fields.Monetary(
        string='Auction Buyout Price',
    )
    product_condition = fields.Selection(
        [('new', 'New'), ('used', 'Used')],
        string='Product Condition',
    )
    carrier_id = fields.Many2one(
        'delivery.carrier',
        string='Delivery Method',
    )
    carrier_size_id = fields.Many2one(
        'delivery.carrier.size',
        string='Delivery Size',
    )
    deliver_prefecture = fields.Char(
        string='Delivery Prefecture',
    )
    delivery_cites = fields.Char(
        string='Delivery Cities',
    )
    yahoo_product_state_id = fields.Many2one(
        'yahoo.product.state',
        string='Yahoo Product State',
    )

    @api.onchange('carrier_id')
    def _onchange_carrier_id(self):
        domain = []
        self.carrier_size_id = False
        if self.carrier_id:
            carrier_sizes = self.env['delivery.carrier.size'].search([
                 ('carrier_id', '=', self.carrier_id.id)
            ])
            domain.append(('id', 'in', carrier_sizes.ids))
        return {'domain': {'carrier_size_id': domain}}
