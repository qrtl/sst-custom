# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_commission = fields.Monetary(
        compute='_compute_amount_commission',
        digits=0,
        string='Commission Amount',
        store=True,
    )

    @api.depends('order_line.price_unit', 'order_line.tax_id', 'order_line.discount', 'order_line.product_uom_qty')
    def _compute_amount_commission(self):
        for order in self:
            order.amount_commission = sum(order.order_line.filtered(
                'is_commission').mapped('price_unit'))

    def update_website_sale_commission(self):
        website_commission_product_id = self.env[
            'ir.config_parameter'].sudo().get_param(
            'website_sale_commission.website_commission_product_id')
        website_commission_percentage = self.env[
            'ir.config_parameter'].sudo().get_param(
            'website_sale_commission.website_commission_percentage')
        if website_commission_product_id:
            if website_commission_percentage:
                chargable_amount = sum(self.order_line.filtered(
                    lambda l: l.product_id.type != 'service').mapped('price_unit'))
                commission_amount = chargable_amount * \
                    float(website_commission_percentage) / 100
            else:
                commission_amount = self.env['product.product'].browse(
                    int(website_commission_product_id)).list_price
            commission_line = self.order_line.filtered(
                lambda l: l.is_commission)
            if not commission_line:
                self.env['sale.order.line'].sudo().create({
                    'order_id': self.id,
                    'is_commission': True,
                    'website_readonly': True,
                    'product_id': int(website_commission_product_id),
                    'product_uom_qty': 1.0,
                    'price_unit': commission_amount,
                })
            else:
                commission_line.sudo().write({
                    'product_id': int(website_commission_product_id),
                    'price_unit': commission_amount,
                })
