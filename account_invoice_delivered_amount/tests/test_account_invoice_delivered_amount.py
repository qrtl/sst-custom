# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAccountInvoiceDeliveredAmount(TransactionCase):
    
    def setUp(cls):
        super(TestAccountInvoiceDeliveredAmount, cls).setUp()
        cls.journal = cls.env["account.journal"].create(
            {"code": "test", "name": "test", "type": "sale"}
        )
        cls.advance_inv_model = cls.env["sale.advance.payment.inv"]
        cls.partner = cls.env.ref("base.res_partner_3")
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "Tax 10",
                "type_tax_use": "sale",
                "amount": 10,
            }
        )
        cls.acc_revenue = cls.env["account.account"].create(
            {
                "code": "X2022",
                "name": "Test Account",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.product_1 = cls.env["product.product"].create(
            {
                "name": "Test",
                "type": "service",
            }
        )
        cls.product_2 = cls.env["product.product"].create(
            {
                "name": "Test Product 2",
                "type": "product",
                "invoice_policy": "order",
            }
        )

    def _create_sale_order(self, include_tax=False):
        so = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )
        self.env["sale.order.line"].create(
            {
                "order_id": so.id,
                "product_id": self.product_1.id,
                "product_uom_qty": 1,
                "price_unit": 100,
                "tax_id": [(6, 0, self.tax.ids)] if include_tax else False,
            }
        )
        self.env["sale.order.line"].create(
            {
                "order_id": so.id,
                "product_id": self.product_2.id,
                "product_uom_qty": 1,
                "price_unit": 200,
                "tax_id": [(6, 0, self.tax.ids)] if include_tax else False,
            }
        )
        so.action_confirm()
        return so

    def test_account_invoice_delivered_amount_without_tax(self):
        order = self._create_sale_order()
        wizard = self.advance_inv_model.create({"advance_payment_method": "delivered"})
        wizard.with_context(
            active_model="sale.order",
            active_ids=[order.id],
            active_id=order.id,
        ).create_invoices()
        invoice = order.invoice_ids
        self.assertEqual(invoice.amount_total_delivered, 100)
        self.assertTrue(invoice.amount_total_delivered_signed > 0)
        self.assertFalse(invoice.delivery_done)

        order.picking_ids.move_lines.write({"quantity_done": 1})
        order.picking_ids.button_validate()
        self.assertEqual(invoice.amount_total_delivered, 300)
        self.assertTrue(invoice.delivery_done)

    def test_account_invoice_delivered_amount_with_tax(self):
        order = self._create_sale_order(include_tax=True)
        wizard = self.advance_inv_model.create({"advance_payment_method": "delivered"})
        wizard.with_context(
            active_model="sale.order",
            active_ids=[order.id],
            active_id=order.id,
        ).create_invoices()
        invoice = order.invoice_ids
        self.assertEqual(invoice.amount_total_delivered, 110)
        self.assertTrue(invoice.amount_total_delivered_signed > 0)
        self.assertFalse(invoice.delivery_done)

        order.picking_ids.move_lines.write({"quantity_done": 1})
        order.picking_ids.button_validate()
        self.assertEqual(invoice.amount_total_delivered, 330)
        self.assertTrue(invoice.delivery_done)
