# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProduct(common.TransactionCase):

    def setUp(self):
        super(TestProduct, self).setUp()
        self.stock_location = self.env.ref('stock.stock_location_stock')

        # Create Test Product
        self.product_01 = self.env['product.product'].create({
            'name': "Test Product 01",
            'type': 'product',
        })

        self.product_02 = self.env['product.product'].create({
            'name': "Test Product 02",
            'type': 'product',
        })
        self.env['stock.quant']._update_available_quantity(self.product_01, self.stock_location, 100)
        self.env['stock.quant']._update_available_quantity(self.product_02, self.stock_location, 100)

        self.product_uom = self.env.ref('product.product_uom_unit').id
        self.sale_order_line = self.env['sale.order.line']
        self.partner_01 = self.env['res.partner'].create({
            'name': 'Test Partner 1',
        })
        self.partner_02 = self.env['res.partner'].create({
            'name': 'Test Partner 2',
        })

    def test_compute_website_sale_available_qty(self):
        """This test evaluate the method whether barcode is updating or not"""

        # I create a sales order
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_01.id,
        })

        # In the sales order I add some sales order lines.
        self.sale_order_line.create({
            'product_id': self.product_01.id,
            'price_unit': 100.00,
            'product_uom': self.product_uom,
            'product_uom_qty': 20.0,
            'order_id': self.sale_order.id,
            'state': 'sent'
        })

        self.sale_order_line.create({
            'product_id': self.product_02.id,
            'price_unit': 100.00,
            'product_uom': self.product_uom,
            'product_uom_qty': 30.0,
            'order_id': self.sale_order.id,
            'state': 'sent'
        })

        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_02.id,
        })

        # In the sales order I add some sales order lines.
        self.sale_order_line.create({
            'product_id': self.product_01.id,
            'price_unit': 100.00,
            'product_uom': self.product_uom,
            'product_uom_qty': 10.0,
            'order_id': self.sale_order.id,
            'state': 'sent'
        })

        self.sale_order_line.create({
            'product_id': self.product_02.id,
            'price_unit': 100.00,
            'product_uom': self.product_uom,
            'product_uom_qty': 25.0,
            'order_id': self.sale_order.id,
            'state': 'sent'
        })

        self.product_01._compute_website_sale_available_qty()

        self.assertEqual(
            self.product_01.website_sale_available_qty,
            70,
            'Check website sale available qty'
        )

        self.product_02._compute_website_sale_available_qty()

        self.assertEqual(
            self.product_02.website_sale_available_qty,
            45,
            'Check website sale available qty'
        )

        self.product_01.product_tmpl_id._compute_website_sale_available_qty()

        self.assertEqual(
            self.product_01.product_tmpl_id.website_sale_available_qty,
            140,
            'Check website sale available qty'
        )

        self.product_02.product_tmpl_id._compute_website_sale_available_qty()

        self.assertEqual(
            self.product_02.product_tmpl_id.website_sale_available_qty,
            90,
            'Check website sale available qty'
        )





        # # Assign Default code to product
        # self.product_01.default_code = 'DEFCODE'
        #
        # # This Method assign value to barcode from default code field
        # self.product_01._compute_barcode()
        #
        # # compare the barcode value which is updated by compute_barcode method.
        # self.assertEqual(
        #     self.product_01.barcode,
        #     'DEFCODE',
        #     'Barcode not used in product name')
