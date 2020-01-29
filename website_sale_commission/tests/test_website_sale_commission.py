# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import ValidationError
from odoo.http import request


class WebsiteSaleCommission(common.TransactionCase):

    def setUp(self):
        super(WebsiteSaleCommission, self).setUp()
        self.test_user = self.env.ref('base.user_demo')
        self.website_sale_order = self.env['sale.order'].sudo(self.test_user.id).create({
            'partner_id': self.test_user.partner_id.id,
            'team_id': self.env.ref('sales_team.salesteam_website_sales').id,
        })
        self.website_commission_product_id = self.env['product.product'].create({
            'name': 'Commission',
            'type': 'service',
            'list_price': 100,
        })
        self.env['ir.config_parameter'].set_param(
            'website_sale_commission.website_commission_product_id', self.website_commission_product_id.id)
        self.product_1 = self.env.ref('product.product_product_8')

    def test_00_add_product_website_order_comission_percentage(self):
        self.env['ir.config_parameter'].set_param(
            'website_sale_commission.website_commission_percentage', 10.0)
        product_order_line = self.env['sale.order.line'].sudo(self.test_user.id).create({
            'product_id': self.product_1.id,
            'name': 'Test Product',
            'price_unit': 100,
            'product_uom_qty': 1.0,
            'order_id': self.website_sale_order.id,
        })
        commission_line = \
            self.website_sale_order.order_line.filtered(
                lambda i: i.is_commission)
        self.assertTrue(commission_line)
        self.assertEqual(commission_line.price_unit,
                         product_order_line.price_unit * 10.0 / 100)

    def test_01_add_product_website_order_fix_comission(self):
        self.env['ir.config_parameter'].set_param(
            'website_sale_commission.website_commission_percentage', False)
        self.env['sale.order.line'].sudo(self.test_user.id).create({
            'product_id': self.product_1.id,
            'name': 'Test Product',
            'price_unit': 100,
            'product_uom_qty': 1.0,
            'order_id': self.website_sale_order.id,
        })
        commission_line = \
            self.website_sale_order.order_line.filtered(
                lambda i: i.is_commission)
        self.assertTrue(commission_line)
        self.assertEqual(commission_line.price_unit,
                         self.website_commission_product_id.list_price)

    def test_02_get_display_price(self):
        self.env['ir.config_parameter'].set_param(
            'website_sale_commission.website_commission_percentage', 10.0)
        self.env['sale.order.line'].sudo(self.test_user.id).create({
            'product_id': self.product_1.id,
            'name': 'Test Product',
            'price_unit': 100,
            'product_uom_qty': 1.0,
            'order_id': self.website_sale_order.id,
        })
        commission_line = \
            self.website_sale_order.order_line.filtered(
                lambda i: i.is_commission)
        self.assertEqual(commission_line._get_display_price(self.website_commission_product_id),
                         commission_line.price_unit)
