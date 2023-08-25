# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProduct(common.TransactionCase):
    def setUp(self):
        super(TestProduct, self).setUp()

        # Create Test Product
        self.product_01 = self.env["product.product"].create({"name": "Test Product"})

    def test_compute_barcode_01(self):
        """This test evaluates the method of
        whether the barcode is updating or not"""

        # Assign Default code to product
        self.product_01.default_code = "DEFCODE"

        # This Method assign value to barcode from default code field
        self.product_01._compute_barcode()

        # compare the barcode value which is updated by compute_barcode method.
        self.assertEqual(
            self.product_01.barcode, "DEFCODE", "Barcode not used in product name"
        )
