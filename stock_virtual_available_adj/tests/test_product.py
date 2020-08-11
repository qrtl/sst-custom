# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProduct(common.TransactionCase):
    def setUp(self):
        super(TestProduct, self).setUp()

        stock_location = self.env.ref("stock.stock_location_stock")
        self.product_uom_id = self.env.ref("product.product_uom_unit").id

        # Create Test Products
        self.product_01 = self.env["product.product"].create(
            {"name": "Test Product 01", "type": "product"}
        )
        self.product_02 = self.env["product.product"].create(
            {"name": "Test Product 02", "type": "product"}
        )
        self.product_03 = self.env["product.product"].create(
            {"name": "Test Product 03", "type": "product"}
        )

        # update the quantity on hand for products
        self.env["stock.quant"]._update_available_quantity(
            self.product_01, stock_location, 100
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product_02, stock_location, 100
        )

        # Create Test Partners
        self.partner_01 = self.env["res.partner"].create({"name": "Test Partner 1"})
        self.partner_02 = self.env["res.partner"].create({"name": "Test Partner 2"})

    def test_compute_website_sale_available_qty_01(self):
        """
            This test compute the website
            sale available quantity for product
        """

        # This test perform to create two sales orders
        # which has few sale order lines and
        # this sale order lines in `draft` and `sent` state.

        # I create a sales order
        self.sale_order_01 = self.env["sale.order"].create(
            {"partner_id": self.partner_01.id}
        )

        # In the sales order I add some sales order lines.
        self.env["sale.order.line"].create(
            {
                "product_id": self.product_01.id,
                "price_unit": 100.00,
                "product_uom": self.product_uom_id,
                "product_uom_qty": 20.0,
                "order_id": self.sale_order_01.id,
            }
        )

        self.env["sale.order.line"].create(
            {
                "product_id": self.product_02.id,
                "price_unit": 100.00,
                "product_uom": self.product_uom_id,
                "product_uom_qty": 30.0,
                "order_id": self.sale_order_01.id,
            }
        )

        # Convert sale-order to sent state
        self.sale_order_01.print_quotation()

        self.sale_order_02 = self.env["sale.order"].create(
            {"partner_id": self.partner_02.id}
        )

        # Draft Order lines
        self.env["sale.order.line"].create(
            {
                "product_id": self.product_02.id,
                "price_unit": 100.00,
                "product_uom": self.product_uom_id,
                "product_uom_qty": 15.0,
                "order_id": self.sale_order_02.id,
                "state": "draft",
            }
        )
        self.env["sale.order.line"].create(
            {
                "product_id": self.product_03.id,
                "price_unit": 100.00,
                "product_uom": self.product_uom_id,
                "product_uom_qty": 10.0,
                "order_id": self.sale_order_02.id,
                "state": "draft",
            }
        )

        # Compare the `draft_sale_qty` qty for product 03(product.product)
        self.assertEqual(
            self.product_03.draft_sale_qty, 10, "Check website draft sale qty",
        )

        self.sale_order_03 = self.env["sale.order"].create(
            {"partner_id": self.partner_02.id}
        )

        # In the sales order I add some sales order lines.
        self.env["sale.order.line"].create(
            {
                "product_id": self.product_01.id,
                "price_unit": 100.00,
                "product_uom": self.product_uom_id,
                "product_uom_qty": 10.0,
                "order_id": self.sale_order_03.id,
            }
        )

        self.env["sale.order.line"].create(
            {
                "product_id": self.product_02.id,
                "price_unit": 100.00,
                "product_uom": self.product_uom_id,
                "product_uom_qty": 25.0,
                "order_id": self.sale_order_03.id,
            }
        )

        # Convert sale-order to sent state
        self.sale_order_03.print_quotation()

        # Compare the `website_sale_available_qty` qty for product 01(product.product)
        self.assertEqual(
            self.product_01.website_sale_available_qty,
            70,
            "Check website sale available qty",
        )

        # Compare the `website_sale_available_qty`
        # qty for product 02(product.product)
        self.assertEqual(
            self.product_02.website_sale_available_qty,
            30,
            "Check website sale available qty",
        )

        # Compare the `website_sale_available_qty`
        # qty for product 01(product.template)
        # (website_sale_available_qty(70) =
        # virtual_available(100.0)-sent_sale_qty(0.0)-draft_sale_qty(30.0))
        self.assertEqual(
            self.product_01.product_tmpl_id.website_sale_available_qty,
            70,
            "Check website sale available qty",
        )

        # Compare the `website_sale_available_qty` qty for product 02(product.template)
        # (website_sale_available_qty(30.0) =
        # virtual_available(100.0) - sent_sale_qty(55.0) - draft_sale_qty(15.0))
        self.assertEqual(
            self.product_02.product_tmpl_id.website_sale_available_qty,
            30,
            "Check website sale available qty",
        )
