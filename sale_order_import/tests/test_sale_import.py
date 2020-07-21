# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import os
import base64
from odoo.tests import common
from odoo.tools.misc import file_open
from odoo.tools.safe_eval import safe_eval


class TestSaleOrderImport(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderImport, self).setUp()
        self.import_sale_obj = self.env['import.sale']
        # Create Test Product
        self.product_01 = self.env['product.product'].create({
            'name': "Product A",
            'type': 'product',
            'default_code': 'ABC'
        })
        # self.partner_delta_id = self.env.ref('base.res_partner_4')
        self.public_pricelist = self.env.ref('product.list0')
        self.warehouse = self.env.ref('stock.warehouse0')
        self.team = self.env.ref("sales_team.team_sales_department")
        self.free_delivery = self.env['ir.model.data'].xmlid_to_res_id(
            'delivery.free_delivery_carrier')
        self.partner_delta_id = self.env['res.partner'].create({
            'name': 'Test Partner',
            'phone': '+1234567890'
        })
        self.customer_phone = '123456789'
        self.cash_journal_cash = self.env['account.journal'].create(
            {'name': 'Cash', 'type': 'cash', 'code': 'CASH'})
        self.note = 'Test Note'

    def test_get_order_dict_flow(self):
        file_path = os.path.join(
            'sale_order_import', 'tests', 'sale_order.csv')
        generated_file = file_open(file_path, 'rb')
        generated_file = generated_file.read()
        wizard_sale = self.env['import.sale'].create({
            'picking_policy': 'direct',
            'customer_invoice_journal_id': self.cash_journal_cash.id,
            'customer_payment_journal_id': self.cash_journal_cash.id,
            'asynchronous': False,
            'input_file': base64.encodestring(generated_file),
            'datas_fname': file_path
        })
        res = wizard_sale.import_sale_data()
        res_domain = safe_eval(res.get('domain', {}))[0][2]

        error_log = self.env['error.log'].browse(res_domain)
        sale_order = error_log.sale_order_ids

        self.assertEqual(
            sale_order.partner_id,
            self.partner_delta_id,
            'From test Sale Order file the "customer"'
            ' does not match with test records'
        )
        self.assertEqual(
            sale_order.partner_invoice_id,
            self.partner_delta_id,
            'Partner Invoice field does not match with Test Partner'
        )
        self.assertEqual(
            sale_order.pricelist_id,
            self.public_pricelist,
            'From test Sale Order file the pricelist'
            ' field data does not match with records')
        self.assertEqual(
            sale_order.partner_shipping_id,
            self.partner_delta_id,
            'Partner shipping field does not match with Test Partner'
        )
        self.assertEqual(
            sale_order.payment_term_id,
            self.partner_delta_id.property_payment_term_id,
            'Sale Order Payment term field data does not match'
            ' with Test Partner Payment term condtion'
        )
        self.assertEqual(
            sale_order.picking_policy,
            'direct',
            'Sale order picking policy value does not match with "direct"'
        )
        self.assertEqual(
            sale_order.team_id,
            self.team,
            'From test Sale Order file the "Team"'
            ' does not match with test records'
        )
        self.assertEqual(
            sale_order.carrier_id.id,
            self.free_delivery,
            'From test Sale Order file the "Carrier"'
            ' does not match with test records'
        )
        self.assertEqual(
            sale_order.warehouse_id,
            self.warehouse,
            'From test Sale Order file the "warehouse" '
            'does not match with test records'
        )
        self.assertEqual(
            sale_order.note,
            self.note,
            'From test Sale Order file the customer does not match with records'
        )

    def test_update_error_log(self):
        file_path = os.path.join(
            'sale_order_import', 'tests', 'sale_order.csv')
        generated_file = file_open(file_path, 'rb')
        generated_file = generated_file.read()
        ir_attachment_obj = self.env["ir.attachment"]
        ir_attachment = ir_attachment_obj.create(
            {
                "name": 'sale_order.csv',
                "datas": base64.encodestring(generated_file),
                "datas_fname": 'sale_order.csv',
            }
        )
        ir_model = self.env['ir.model'].search([('name', '=', 'sale.order')])
        import_log_id = self.import_sale_obj._update_error_log(
            error_log_id=False,
            error_vals={
                'error': 'Data not found',
                'error_name': 'Test Product Does not found',
            },
            ir_attachment=ir_attachment,
            model=ir_model,
            row_no=2,
            order_group_value=1
        )
        error_log_id = self.env['error.log'].search([
            ('model_id', '=', ir_model.id),
            ('state', '=', 'failed')
        ])

        self.assertEqual(
            error_log_id.input_file,
            ir_attachment,
            'Check the uploaded attachment'
        )
        self.assertEqual(
            error_log_id.import_user_id,
            self.env.user,
            'Check the environment user seems not different'
        )

        self.import_sale_obj._update_error_log(
            error_log_id=import_log_id,
            error_vals={
                'error': 'Data not found',
                'error_name': 'Test Product B Does not found',
            },
            ir_attachment=None,
            model=None,
            row_no=2,
            order_group_value=None
        )

        log_line = self.env["error.log.line"].search([
            ('log_id', '=', error_log_id.id)
        ])

        self.assertEqual(
            len(log_line),
            2,
            'Check number of records for log line')
