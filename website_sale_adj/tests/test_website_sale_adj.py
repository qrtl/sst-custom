# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time

from odoo.tests import common
from odoo.addons.website_sale_adj.controllers.main import WebsiteSale


class WebsiteSaleAdj(common.TransactionCase):

    def setUp(self):
        super(WebsiteSaleAdj, self).setUp()
        self.product_1 = self.env.ref(
            'product.product_product_8').product_tmpl_id
        self.product_2 = self.env.ref(
            'product.product_product_9').product_tmpl_id
        self.product_3 = self.env.ref(
            'product.product_product_10').product_tmpl_id
        self.product_list = self.product_1 + self.product_2 + self.product_3
        self.product_list.update({
            "website_published": False
        })

    def test_00_publish_product(self):
        self.product_3.update({
            "website_published": True
        })
        time.sleep(1)
        self.product_2.update({
            "website_published": True
        })
        time.sleep(1)
        self.product_1.update({
            "website_published": True
        })
        product_order_list = self.env['product.template'].search(
            [], order=WebsiteSale._get_search_order(self, {}))
        self.assertEqual(product_order_list[0], self.product_1)
        self.assertEqual(product_order_list[1], self.product_2)
        self.assertEqual(product_order_list[2], self.product_3)

    def test_01_update_list_price(self):
        self.product_list.update({
            "website_published": True
        })
        self.product_1.update({
            "list_price": 100
        })
        time.sleep(1)
        self.product_2.update({
            "list_price": 200
        })
        time.sleep(1)
        self.product_3.update({
            "list_price": 300
        })
        product_order_list = self.env['product.template'].search(
            [], order=WebsiteSale._get_search_order(self, {}))
        self.assertEqual(product_order_list[0], self.product_3)
        self.assertEqual(product_order_list[1], self.product_2)
        self.assertEqual(product_order_list[2], self.product_1)

    def test_02_update_website_sequence_date(self):
        self.product_list.update({
            "website_published": True
        })
        self.product_1._update_website_sequence_date()
        time.sleep(1)
        self.product_3._update_website_sequence_date()
        time.sleep(1)
        self.product_2._update_website_sequence_date()
        product_order_list = self.env['product.template'].search(
            [], order=WebsiteSale._get_search_order(self, {}))
        self.assertEqual(product_order_list[0], self.product_2)
        self.assertEqual(product_order_list[1], self.product_3)
        self.assertEqual(product_order_list[2], self.product_1)

    def test_03_create_product(self):
        product_1 = self.env['product.template'].create({
            'name': 'Test 001',
            'website_published': True,
        })
        product_2 = self.env['product.template'].create({
            'name': 'Test 002',
            'website_published': True,
        })
        product_3 = self.env['product.template'].create({
            'name': 'Test 002',
            'website_published': True,
        })
        product_order_list = self.env['product.template'].search(
            [], order=WebsiteSale._get_search_order(self, {}))
        self.assertEqual(product_order_list[0], product_3)
        self.assertEqual(product_order_list[1], product_2)
        self.assertEqual(product_order_list[2], product_1)
