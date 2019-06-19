# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def write(self, vals):
        if 'state' in vals:
            for order in self:
                if order.team_id.team_type == 'website':
                    for order_line in order.order_line:
                        order_line.product_id.in_cart = False
        res =  super(SaleOrder, self).write(vals)
        if 'state' in vals:
            for order in self:
                if order.team_id.team_type == 'website' and order.state != \
                        'cancel':
                    for order_line in order.order_line:
                        order_line.product_id.in_cart = True
        return res

    @api.multi
    def unlink(self):
        for order in self:
            for order_line in order.order_line:
                order_line.product_id.in_cart = False
        return super(SaleOrder, self).unlink()
