# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_commission = fields.Boolean(string="Is Commission", default=False)

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        if 'product_uom_qty' in vals or 'price_unit' in vals or 'tax_id' in \
                vals or 'discount' in vals:
            for order_line in self:
                if order_line.order_id.state == 'draft' and \
                    order_line.product_id.type != 'service' and \
                        order_line.order_id.team_id and \
                        order_line.order_id.team_id.team_type == 'website':
                    order_line.order_id.update_website_sale_commission()
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        for order_line in res:
            if order_line.order_id.state == 'draft' and \
                order_line.product_id.type != 'service' and \
                    order_line.order_id.team_id and \
                    order_line.order_id.team_id.team_type == 'website':
                order_line.order_id.update_website_sale_commission()
        return res

    @api.multi
    def unlink(self):
        orders = self.mapped('order_id')
        update_flag = self.filtered(lambda l: not l.is_commission)
        res = super(SaleOrderLine, self).unlink()
        if update_flag:
            for order in orders.filtered(
                lambda o: o.team_id and o.state == 'draft' and
                    o.team_id.team_type == 'website'):
                order.update_website_sale_commission()
        return res
