# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64
import os

from odoo.tests import common
from odoo.tools.misc import file_open
from odoo.tools.safe_eval import safe_eval


class TestSaleOrderImport(common.TransactionCase):
    """
    This tests class perform the tests for the following points:
        - Checking the to import file
        test_regular_sale_order.csv(/sale_order_import/
        tests/test_regular_sale_order.csv) and add the sale order from file.
        - Checking the error while import file test_regular_sale_order.csv
    """

    def setUp(self):
        super(TestSaleOrderImport, self).setUp()
        # Create Test Partner
        self.partner_01 = self.env["res.partner"].create(
            {"name": "Test Partner 01", "phone": "1234567890", "mobile": "1234567890"}
        )
        self.partner_02 = self.env["res.partner"].create(
            {"name": "Test Partner 02", "phone": "9876543210", "mobile": "9876543210"}
        )

        # Create Test Product
        self.product_01 = self.env["product.product"].create(
            {"name": "Product A", "type": "product", "default_code": "ABC"}
        )
        self.product_02 = self.env["product.product"].create(
            {"name": "Product B", "type": "product", "default_code": "XYZ"}
        )
        self.product_03 = self.env["product.product"].create(
            {"name": "Product C", "type": "product", "default_code": "ZYX"}
        )

        self.public_pricelist = self.env.ref("product.list0")
        self.warehouse = self.env.ref("stock.warehouse0")
        self.team = self.env.ref("sales_team.crm_team_1")
        self.free_delivery_id = self.env["ir.model.data"].xmlid_to_res_id(
            "delivery.free_delivery_carrier"
        )
        self.cash_journal_cash = self.env["account.journal"].create(
            {"name": "Cash", "type": "cash", "code": "CASH"}
        )
        self.note = "Test Note"

    def test_01_get_order_dict_flow(self):
        """
            This test evaluates the import test sales order CSV
             file and compares the values with test records.
        """

        # Check the file path and load the test_regular_sale_order.csv
        file_path = os.path.join(
            "sale_order_import", "tests", "test_regular_sale_order.csv"
        )
        generated_file = file_open(file_path, "rb")
        generated_file = generated_file.read()

        # Note: Here I have called `import_sale_data` method which is the main
        # method of sale order CSV file. This method covers the
        # '  get_order_dict' method flow and their values.
        # And here I am not going to call the method get_order_dict because
        # this method many arguments and contains the dynamic value
        # which is not possible to make in a short time. so, for now,
        # I have called `import_sale_data` method which covers this method and
        # dynamic values, Here also compares the
        # values which return by `get_order_dict`.
        # https://github.com/qrtl/sst-custom/blob/11.0/sale_order_import/wizard/import_sale.py#L240 # noqa

        # Create wizard where the add test_regular_sale_order.csv
        # and allow to import sale order data.
        wizard_sale = self.env["import.sale"].create(
            {
                "picking_policy": "direct",
                "customer_invoice_journal_id": self.cash_journal_cash.id,
                "customer_payment_journal_id": self.cash_journal_cash.id,
                "asynchronous": False,
                "input_file": base64.encodestring(generated_file),
                "datas_fname": file_path,
            }
        )

        # The Main Method called import_sale_data.
        res = wizard_sale.import_sale_data()

        # `import_sale_data method returns the actions
        # So here I am taking the domain which
        # contains the `ids` of error.log object.
        res_domain = safe_eval(res.get("domain", {}))[0][2]

        # Browse the error.log object ids which return in res_domain
        error_log = self.env["error.log"].browse(res_domain)
        sale_order = error_log.sale_order_ids
        # Sample data from test_regular_sale_order.csv file
        # Line Product,Line Description,Line Unit Price,Line Qty,Customer,\
        # Pricelist,Warehouse,Notes,Carrier,Team,Customer Phone/Mobile
        # ABC,Product A,200,2,,Test Partner,Public Pricelist,\
        # My Company,Test Note,Free delivery charges,Sales,+1234567890

        # Compares the values with test_regular_sale_order.csv file.
        self.assertEqual(sale_order[0].partner_id, self.partner_02)
        self.assertEqual(sale_order[1].partner_id, self.partner_01)
        self.assertEqual(
            sale_order[0].partner_invoice_id,
            self.partner_02,
            "Partner Invoice field id is incorrect for sale_order[0]",
        )
        self.assertEqual(
            sale_order[1].partner_invoice_id,
            self.partner_01,
            "Partner Invoice field id is incorrect for sale_order[1]",
        )
        self.assertEqual(
            sale_order[0].pricelist_id,
            self.public_pricelist,
            "From test Sale Order file the pricelist"
            " field data does not match with records",
        )
        self.assertEqual(
            sale_order[0].partner_shipping_id,
            self.partner_02,
            "Partner shipping field does not match with Test Partner",
        )
        self.assertEqual(
            sale_order[1].partner_shipping_id,
            self.partner_01,
            "Partner shipping field does not match with Test Partner",
        )
        self.assertEqual(
            sale_order[0].payment_term_id,
            self.partner_02.property_payment_term_id,
            "Sale Order Payment term field data does not match"
            " with Test Partner Payment term condition",
        )
        self.assertEqual(
            sale_order[0].picking_policy,
            "direct",
            'Sale order picking policy value does not match with "direct"',
        )
        self.assertEqual(
            sale_order[0].team_id,
            self.team,
            "From test Sale Order file the 'Team' does not match with test records",
        )
        self.assertEqual(
            sale_order[0].carrier_id.id,
            self.free_delivery_id,
            'From test Sale Order file the "Carrier"'
            " does not match with test records",
        )
        self.assertEqual(
            sale_order[0].warehouse_id,
            self.warehouse,
            'From test Sale Order file the "warehouse" '
            "does not match with test records",
        )
        self.assertEqual(
            sale_order[0].note,
            self.note,
            "From test Sale Order file the customer does not match with records",
        )

    def test_02_update_error_log(self):
        """
            Importing test_error_sale_order.csv file which has
             some errors and compares their errors..
        """

        # Check the file path and load the test_regular_sale_order.csv
        file_path = os.path.join(
            "sale_order_import", "tests", "test_error_sale_order.csv"
        )
        generated_file = file_open(file_path, "rb")
        generated_file = generated_file.read()

        wizard_sale = self.env["import.sale"].create(
            {
                "picking_policy": "direct",
                "customer_invoice_journal_id": self.cash_journal_cash.id,
                "customer_payment_journal_id": self.cash_journal_cash.id,
                "asynchronous": False,
                "input_file": base64.encodestring(generated_file),
                "datas_fname": file_path,
            }
        )

        # The Main Method called import_sale_data.
        wizard_sale.import_sale_data()

        # Search the error log which is created by `update_error_log`
        error_log_id = self.env["error.log"].search([("state", "=", "failed")])

        # Compare the errors name while importing the test_error_sale_order.csv.
        self.assertEqual(
            error_log_id.log_line_ids[0].error_name, "Product: NPD Not Found!\n"
        )

        # Compare the row no from the error sale order csv file..
        self.assertEqual(error_log_id.log_line_ids[0].row_no, 2)

        # Compare the group number from the error sale order csv file..
        self.assertEqual(error_log_id.log_line_ids[0].order_group, "1")

        # Compare the errors name while importing the test_error_sale_order.csv.
        self.assertEqual(
            error_log_id.log_line_ids[1].error_name, "Product: JKL Not Found!\n"
        )

        # Compare the row no from the error sale order csv file..
        self.assertEqual(error_log_id.log_line_ids[1].row_no, 3)

        # Compare the group number from the error sale order csv file..
        self.assertEqual(error_log_id.log_line_ids[1].order_group, "2")

        # Compare the length of error log lines records.
        self.assertEqual(
            len(error_log_id.log_line_ids), 2, "Check number of records for log line"
        )
