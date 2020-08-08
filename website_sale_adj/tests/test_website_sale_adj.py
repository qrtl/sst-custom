# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import time

from odoo.tests import common

from odoo.addons.website_sale_adj.controllers.main import WebsiteSale


class WebsiteSaleAdj(common.TransactionCase):
    def setUp(self):
        super(WebsiteSaleAdj, self).setUp()
        self.product_1 = self.env.ref("product.product_product_8").product_tmpl_id
        self.product_2 = self.env.ref("product.product_product_9").product_tmpl_id
        self.product_3 = self.env.ref("product.product_product_10").product_tmpl_id
        self.product_list = self.product_1 + self.product_2 + self.product_3
        self.product_list.update({"website_published": False})

    def test_00_publish_product(self):
        self.product_3.update({"website_published": True})
        time.sleep(1)
        self.product_2.update({"website_published": True})
        time.sleep(1)
        self.product_1.update({"website_published": True})
        product_order_list = self.env["product.template"].search(
            [], order=WebsiteSale._get_search_order(self, {})
        )
        self.assertEqual(product_order_list[0], self.product_1)
        self.assertEqual(product_order_list[1], self.product_2)
        self.assertEqual(product_order_list[2], self.product_3)

    def test_01_update_list_price(self):
        self.product_list.update({"website_published": True})
        self.product_1.update({"list_price": 100})
        time.sleep(1)
        self.product_2.update({"list_price": 200})
        time.sleep(1)
        self.product_3.update({"list_price": 300})
        product_order_list = self.env["product.template"].search(
            [], order=WebsiteSale._get_search_order(self, {})
        )
        self.assertEqual(product_order_list[0], self.product_3)
        self.assertEqual(product_order_list[1], self.product_2)
        self.assertEqual(product_order_list[2], self.product_1)

    def test_02_update_website_sequence_date(self):
        self.product_list.update({"website_published": True})
        self.product_1._update_website_sequence_date()
        time.sleep(1)
        self.product_3._update_website_sequence_date()
        time.sleep(1)
        self.product_2._update_website_sequence_date()
        product_order_list = self.env["product.template"].search(
            [], order=WebsiteSale._get_search_order(self, {})
        )
        self.assertEqual(product_order_list[0], self.product_2)
        self.assertEqual(product_order_list[1], self.product_3)
        self.assertEqual(product_order_list[2], self.product_1)

    def test_03_create_product(self):
        product_1 = self.env["product.template"].create(
            {"name": "Test 001", "website_published": True}
        )
        product_2 = self.env["product.template"].create(
            {"name": "Test 002", "website_published": True}
        )
        product_3 = self.env["product.template"].create(
            {"name": "Test 003", "website_published": True}
        )
        product_order_list = self.env["product.template"].search(
            [], order=WebsiteSale._get_search_order(self, {})
        )
        self.assertEqual(product_order_list[0], product_3)
        self.assertEqual(product_order_list[1], product_2)
        self.assertEqual(product_order_list[2], product_1)

    def test_04_compute_order_line_date(self):
        """
            This tests check the earliest
            website_order_line's creation date
            """
        self.product_uom = self.env.ref("product.product_uom_unit").id

        # Create Test Product
        self.product_01 = self.env["product.product"].create(
            {"name": "Test Product 1", "type": "product"}
        )
        self.product_02 = self.env["product.product"].create(
            {"name": "Test Product 2", "type": "product"}
        )

        # Create Test Partner
        self.partner_01 = self.env["res.partner"].create({"name": "Test Partner 1"})

        # Create sale order
        self.sale_order = self.env["sale.order"].create(
            {"partner_id": self.partner_01.id}
        )

        # Create Sale Order line
        line_01 = self.env["sale.order.line"].create(
            {
                "product_id": self.product_01.id,
                "price_unit": 100.00,
                "product_uom": self.product_uom,
                "product_uom_qty": 10.0,
                "order_id": self.sale_order.id,
            }
        )
        line_02 = self.env["sale.order.line"].create(
            {
                "product_id": self.product_02.id,
                "price_unit": 200.00,
                "product_uom": self.product_uom,
                "product_uom_qty": 20.0,
                "order_id": self.sale_order.id,
            }
        )

        # Assign website order line from sale order line
        self.sale_order.write(
            {"website_order_line": [(6, 0, [line_01.id, line_02.id])]}
        )

        # Compute the `_compute_order_line_date`
        self.sale_order._compute_order_line_date()

        # Compare the `order_line_date` with sale order line create_date.
        self.assertEqual(
            self.sale_order.order_line_date,
            line_01.create_date,
            "Check the Sale Order --> Order line date"
            " does not match with line create date",
        )
