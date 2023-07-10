# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProductGrossProfitCalculation(common.TransactionCase):
    def setUp(self):
        super(TestProductGrossProfitCalculation, self).setUp()
        self.test_sale_order = self.env["sale.order"]
        self.test_user = self.env.ref("base.user_demo")
        self.product_1 = self.env.ref("product.product_product_8")
        self.tax_10pc_excl = self.env["account.tax"].create(
            {
                "name": "Tax 10%",
                "amount_type": "percent",
                "amount": 10,
                "type_tax_use": "sale",
            }
        )
        self.tax_10pc_incl = self.env["account.tax"].create(
            {
                "name": "10% Tax incl",
                "amount_type": "percent",
                "amount": 10,
                "price_include": True,
            }
        )
        self.invoice_account = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_receivable").id,
                )
            ],
            limit=1,
        )

    def test_00_sale_price_unit_update_tax_excl(self):
        # Create sale order with tax included order line
        self.test_sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.test_user.partner_id.id,
                "team_id": self.env.ref("sales_team.salesteam_website_sales").id,
            }
        )
        self.env["sale.order.line"].create(
            {
                "product_id": self.product_1.id,
                "name": "Test Product",
                "price_unit": 100,
                "product_uom_qty": 2.0,
                "order_id": self.test_sale_order.id,
                "tax_id": [(6, 0, [self.tax_10pc_excl.id])],
            }
        )
        # Confirm sale order and the sale_price_unit of the product should be updated
        self.test_sale_order.action_confirm()
        self.assertEqual(self.product_1.product_tmpl_id.sale_price_unit, 110)

        # Create invoice with tax included invoice line
        test_invoice = self.env["account.move"].create(
            {
                "partner_id": self.test_user.partner_id.id,
                "account_id": self.invoice_account.id,
                "move_type": "out_invoice",
            }
        )
        self.env["account.move.line"].create(
            {
                "product_id": self.product_1.id,
                "name": "Test Product",
                "price_unit": 200,
                "quantity": 2.0,
                "move_id": test_invoice.id,
                "tax_ids": [(6, 0, [self.tax_10pc_excl.id])],
                "account_id": self.invoice_account.id,
            }
        )
        # Validate invoice and the sale_price_unit of the product should be updated
        test_invoice.action_post()
        self.assertEqual(self.product_1.product_tmpl_id.sale_price_unit, 220)

        # Update sale_price_unit manually and reset it by _update_sale_price_unit()
        self.product_1.product_tmpl_id.sale_price_unit = 0
        self.product_1.product_tmpl_id._update_sale_price_unit()
        self.assertEqual(self.product_1.product_tmpl_id.sale_price_unit, 220)

    def test_01_sale_price_unit_update_tax_incl(self):
        # Create sale order with tax excluded order line
        self.test_sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.test_user.partner_id.id,
                "team_id": self.env.ref("sales_team.salesteam_website_sales").id,
            }
        )
        self.env["sale.order.line"].create(
            {
                "product_id": self.product_1.id,
                "name": "Test Product",
                "price_unit": 100,
                "product_uom_qty": 2.0,
                "order_id": self.test_sale_order.id,
                "tax_id": [(6, 0, [self.tax_10pc_incl.id])],
            }
        )
        # Confirm sale order and the sale_price_unit of the product should be updated
        self.test_sale_order.action_confirm()
        self.assertEqual(self.product_1.product_tmpl_id.sale_price_unit, 100)

        # Create invoice with tax excluded invoice line
        test_invoice = self.env["account.move"].create(
            {
                "partner_id": self.test_user.partner_id.id,
                "account_id": self.invoice_account.id,
                "move_type": "out_invoice",
            }
        )
        self.env["account.move.line"].create(
            {
                "product_id": self.product_1.id,
                "name": "Test Product",
                "price_unit": 200,
                "quantity": 2.0,
                "invoice_id": test_invoice.id,
                "tax_ids": [(6, 0, [self.tax_10pc_incl.id])],
                "account_id": self.invoice_account.id,
            }
        )
        # Validate invoice and the sale_price_unit of the product should be updated
        test_invoice.action_post()
        self.assertEqual(self.product_1.product_tmpl_id.sale_price_unit, 200)

        # Update sale_price_unit manually and reset it by _update_sale_price_unit()
        self.product_1.product_tmpl_id.sale_price_unit = 0
        self.product_1.product_tmpl_id._update_sale_price_unit()
        self.assertEqual(self.product_1.product_tmpl_id.sale_price_unit, 200)
