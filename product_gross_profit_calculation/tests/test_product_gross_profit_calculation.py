# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import common


class TestProductGrossProfitCalculation(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductGrossProfitCalculation, cls).setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test",
                "categ_id": cls.env.ref("product.product_category_all").id,
                "standard_price": 50,
                "list_price": 100,
                "type": "service",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "uom_po_id": cls.env.ref("uom.product_uom_unit").id,
                "description": "Test",
                "taxes_id": [],
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {"code": "test", "name": "test", "type": "sale"}
        )

    def test_sale_order_confirmation(self):
        # Create sale order
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_12").id,
                "team_id": self.env.ref("sales_team.crm_team_1").id,
            }
        )
        # Create sale order line
        self.env["sale.order.line"].create(
            {
                "product_id": self.product.id,
                "name": "Test Product",
                "price_unit": 200,
                "product_uom_qty": 2.0,
                "order_id": sale_order.id,
            }
        )
        sale_order.action_confirm()
        self.assertEqual(self.product.sale_price_unit, 200)
        self.assertEqual(self.product.confirmation_date, sale_order.date_order)
        self.assertEqual(self.product.team_id.id, sale_order.team_id.id)

    def test_invoice_posting(self):
        # Create invoice
        income_account = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.env.ref("base.res_partner_12").id,
                "move_type": "out_invoice",
                "journal_id": self.journal.id,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": "Test Product",
                            "price_unit": 400,
                            "quantity": 2.0,
                            "account_id": income_account.id,
                        },
                    )
                ],
            }
        )
        # Post invoice and check the sale_price_unit of the product
        invoice.action_post()
        self.assertEqual(self.product.sale_price_unit, 400)
