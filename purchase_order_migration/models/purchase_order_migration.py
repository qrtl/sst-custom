# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api, models


class PurchaseOrderMigration(models.Model):
    _name = "purchase.order.migration"
    _inherit = ["data.migration", "data.migration.mapping"]
    _description = "Purchase Order Data Migration"

    def get_or_create_dummy_product(self):
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
        # Check if the dummy product already exists
        dummy_product = env['product.product'].search([('default_code', '=', 'DUMMY_PRODUCT')], limit=1)
        if dummy_product:
            return dummy_product.id
        else:
            # If the dummy product does not exist, create it
            dummy_product = env['product.product'].create({
                'name': 'Dummy Product',
                'type': 'product',
                'default_code': 'DUMMY_PRODUCT',
                'taxes_id': False,  # Assuming no taxes, adjust if necessary
            })
            return dummy_product.id

    def _run_purchase_order_data_migration(self):
        required_fields = [
            "id",
            "origin",
            "partner_ref",
            "date_order",
            "date_approve",
            "partner_id",
            "dest_address_id",
            "currency_id",
            "state",
            "notes",
            "date_planned",
            "amount_untaxed",
            "amount_tax",
            "amount_total",
            "fiscal_position_id",
            "payment_term_id",
            "incoterm_id",
            "company_id",
            "address",
            "remark",
            "sale_prediction_amount",
            "request_channel_id",
            "request_medium_id",
            "call_back",
            "state_id",
            "city",
            "street",
            "street2",
            "zip",
            "phone_update",
            "phone_search",
            "supplier_phone",
            "supplier_mobile",
            "tentative_name",
            "purchase_category_id",
            "employee_id",
            "shop_id",
            "purchase_by_id",
            "allow_convert",
            # 'sale_order_id', # To check need to migrate or not
        ]
        instance, uid_v11, models_v11 = self._data_migration_authentication()
        offset = 0
        limit = 1000
        while True:
            purchase_order_v11 = models_v11.execute_kw(
                instance.instance_db,
                uid_v11,
                instance.password,
                "purchase.order",
                "search_read",
                [],
                {"fields": required_fields, "offset": offset, "limit": limit},
            )
            if not purchase_order_v11:
                break
            offset += limit

            for purchase in purchase_order_v11:
                self.with_delay()._process_purchase_order_migration(purchase)

    def _process_purchase_order_migration(self, purchase):
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
        many2one_field_mapping = {
            "incoterm_id": "account.incoterms",
            "fiscal_position_id": "account.fiscal.position",
            "company_id": "res.company",
            "payment_term_id": "account.payment.term",
            "currency_id": "res.currency",
            "dest_address_id": "res.partner",
            "partner_id": "res.partner",
            "request_channel_id": "request.channel",
            "request_medium_id": "request.medium",
            "purchase_category_id": "purchase.category",
            "employee_id": "hr.employee",
            "shop_id": "stock.warehouse",
            "purchase_by_id": "hr.employee",
            "state_id": "res.country.state",
            # 'sale_order_id': 'sale.order',
        }
        for field, model in many2one_field_mapping.items():
            if field in purchase:
                purchase[field] = self.map_many2one_field_by_name(
                    env, model, purchase[field]
                )

        purchase["old_id"] = purchase["id"]
        order = env["purchase.order"].create(purchase)
        self.create_purchase_order_line(order)
        order.write(
            {
                "amount_tax": purchase["amount_tax"],
                "amount_untaxed": purchase["amount_untaxed"],
                "amount_total": purchase["amount_total"],
            }
        )

    def create_purchase_order_line(self, order):
        required_fields = [
            "account_analytic_id",
            "analytic_tag_ids",
            "company_id",
            "date_planned",
            "name",
            "price_subtotal",
            "price_tax",
            "price_total",
            "price_unit",
            "product_qty",
            "product_uom",
            "qty_invoiced",
            "qty_received",
            "taxes_id",
        ]

        instance, uid_v11, models_v11 = self._data_migration_authentication()
        purchase_order_line_v11 = models_v11.execute_kw(
            instance.instance_db,
            uid_v11,
            instance.password,
            "purchase.order.line",
            "search_read",
            [],
            {"fields": required_fields, "domain": [("order_id", "=", order.old_id)]},
        )
        for line in purchase_order_line_v11:
            env = api.Environment(self.env.cr, SUPERUSER_ID, {})
            many2one_field_mapping = {
                "account_analytic_id": "account.analytic.account",
                "analytic_tag_ids": "account.analytic.tag",
                "company_id": "res.company",
                "product_uom": "uom.uom",
            }
            dummy_product_id = self.get_or_create_dummy_product()
            line["product_id"] = dummy_product_id
            for field, model in many2one_field_mapping.items():
                if field in line and line[field]:
                    line[field] = self.map_many2one_field_by_name(
                        env, model, line[field]
                    )
            for field, value in list(line.items()):
                if isinstance(value, tuple) or isinstance(value, list):
                    line.pop(field, None)

            line["order_id"] = order.id
            order_line = env["purchase.order.line"].create(line)
            order_line.taxes_id = False
            order_line.write({"price_tax": line["price_tax"]})
