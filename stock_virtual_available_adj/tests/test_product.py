# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProduct(common.TransactionCase):
    def setUp(self):
        super().setUp()

        stock_location = self.env.ref("stock.stock_location_stock")
        product_product = self.env["product.product"]
        stock_quant = self.env["stock.quant"]

        self.product_01 = product_product.create(
            {"name": "Test Product 01", "type": "product"}
        )
        self.product_02 = product_product.create(
            {"name": "Test Product 02", "type": "product"}
        )
        self.product_03 = product_product.create(
            {"name": "Test Product 03", "type": "product"}
        )

        # Create stock for products
        stock_quant._update_available_quantity(self.product_01, stock_location, 100.0)
        stock_quant._update_available_quantity(self.product_02, stock_location, 100.0)

        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

    def test_01_compute_website_sale_available_qty(self):
        sale_order = self.env["sale.order"]

        def _create_line(product, qty, order):
            return self.env["sale.order.line"].create(
                {
                    "product_id": product.id,
                    "price_unit": 10.00,
                    "product_uom": product.uom_id.id,
                    "product_uom_qty": qty,
                    "order_id": order.id,
                }
            )

        # Create an order with 'draft' state
        sale_order_01 = sale_order.create({"partner_id": self.partner.id})
        _create_line(self.product_01, 20.0, sale_order_01)
        _create_line(self.product_02, 30.0, sale_order_01)

        # Create an order with 'draft' state
        sale_order_02 = sale_order.create({"partner_id": self.partner.id})
        _create_line(self.product_01, 15.0, sale_order_02)

        # Create an order with 'sent' state
        sale_order_03 = sale_order.create({"partner_id": self.partner.id})
        _create_line(self.product_02, 10.0, sale_order_03)
        sale_order_03.print_quotation()

        self.assertEqual(self.product_01.draft_sale_qty, 35.0)
        self.assertEqual(self.product_01.sent_sale_qty, 0.0)
        self.assertEqual(self.product_02.draft_sale_qty, 30.0)
        self.assertEqual(self.product_02.sent_sale_qty, 10.0)

        # Check the result at product variant level
        self.assertEqual(self.product_01.website_sale_available_qty, 65.0)
        self.assertEqual(self.product_02.website_sale_available_qty, 60.0)

        # Check the result at product template level
        self.assertEqual(
            self.product_01.product_tmpl_id.website_sale_available_qty, 65.0,
        )
        self.assertEqual(
            self.product_02.product_tmpl_id.website_sale_available_qty, 60.0,
        )
