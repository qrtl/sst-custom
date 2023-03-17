# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import io
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import pycompat

FIELD_KEYS = {0: "field", 1: "label", 2: "field_type", 3: "required"}
FIELD_VALS = [
    ["order_group", "Group", "float", True],
    ["product_id", "Line Product", "char", True],
    ["line_name", "Line Description", "char", False],
    ["price_unit", "Line Unit Price", "float", True],
    ["product_qty", "Line Qty", "float", True],
    ["taxes_id", "Line Tax", "char", False],
    ["partner_name", "Customer", "char", True],
    ["pricelist_id", "Pricelist", "char", True],
    ["warehouse_id", "Warehouse", "char", True],
    ["notes", "Notes", "char", False],
    ["carrier_id", "Carrier", "char", False],
    ["team_id", "Team", "char", True],
    ["partner_tel", "Customer Phone/Mobile", "char", True],
]
FIELDS_TO_IMPORT = [
    "Group",
    "Customer",
    "Customer Phone/Mobile",
    "Line Product",
    "Line Description",
    "Line Unit Price",
    "Line Qty",
    "Line Tax",
    "Notes",
    "Pricelist",
    "Warehouse",
    "Team",
    "Carrier",
]


class ImportSale(models.TransientModel):
    _name = "import.sale"
    _inherit = "data.import"

    @api.model
    def _default_picking_policy(self):
        """Get picking policy"""
        return self.env.company.picking_policy

    @api.model
    def _default_customer_invoice_journal(self):
        """Get customer invoice journal"""
        return self.env.company.customer_invoice_journal_id

    @api.model
    def _default_customer_payment_journal(self):
        """Get customer payment journal"""
        return self.env.company.customer_payment_journal_id

    input_file = fields.Binary(
        string="Sale Order File (.csv Format)",
        required=True,
    )
    datas_fname = fields.Char(string="File Path")
    picking_policy = fields.Selection(
        [("direct", "As soon as possible"), ("one", "When all products are ready")],
        string="Shipping Policy",
        required=True,
        default=_default_picking_policy,
    )
    customer_invoice_journal_id = fields.Many2one(
        "account.journal",
        string="Customer Invoice Journal",
        required=True,
        default=_default_customer_invoice_journal,
    )
    customer_payment_journal_id = fields.Many2one(
        "account.journal",
        string="Customer Payment Journal",
        default=_default_customer_payment_journal,
    )
    asynchronous = fields.Boolean(string="Import Asynchronously", default=True)
    process_payment = fields.Boolean("Process Payments")

    @api.model
    def _get_order_value_dict(
        self,
        error_vals,
        partner_tel,
        product_id,
        pricelist_id,
        warehouse_id,
        team_id,
        carrier_id,
        partner_dict,
        product_dict,
        pricelist_dict,
        picking_dict,
        warehouse_dict,
        team_dict,
        carrier_dict,
    ):
        partner_value = partner_tel
        partner_name = self._context.get("partner_name")
        if partner_name:
            self = self.with_context(partner_name=partner_name.strip())
        self._get_partner_dict(partner_value, partner_dict)

        product_id_value = product_id
        self._get_product_dict(product_id_value, product_dict, error_vals)

        pricelist_value = pricelist_id
        self._get_pricelist_dict(pricelist_value, pricelist_dict, error_vals)

        warehouse_value = warehouse_id
        self._get_picking_dict(
            warehouse_value, picking_dict, warehouse_dict, error_vals
        )

        team_value = team_id
        self._get_team_dict(team_value, team_dict, error_vals)

        carrier_value = carrier_id
        if carrier_value:
            self._get_carrier_dict(carrier_value, carrier_dict, error_vals)

        return (
            partner_value,
            product_id_value,
            pricelist_value,
            warehouse_value,
            team_value,
            carrier_value,
        )

    @api.model
    def _get_order_value(self, error_vals, taxes, taxes_id, price_unit, product_qty):
        tax_from_chunk = taxes_id
        if tax_from_chunk:
            self._get_taxes(tax_from_chunk, taxes, error_vals)
        price_unit = float(price_unit)
        product_qty = float(product_qty)
        for k, v in {_("Quantity"): product_qty, _("Unit Price"): price_unit}.items():
            if v > 0:
                continue
            error_vals["error_message"] = (
                error_vals["error_message"]
                + _("Value must be greater than 0: %s") % k
                + "\n"
            )
            error_vals["error"] = True
        return product_qty, price_unit

    @api.model
    def _get_order_item_dict(
        self,
        data_import_log_id,
        order,
        taxes,
        line_name,
        product_dict,
        product_id_value,
        order_item_dict,
        qty,
        price_unit_value,
    ):
        if not data_import_log_id:
            name = line_name
            product_data = self.env["product.product"].browse(
                product_dict[product_id_value]
            )
            if not name:
                name = product_data.name

            invoiceable = True
            if product_data.invoice_policy == "delivery":
                invoiceable = False

            state = "draft"
            if order not in order_item_dict.keys():
                order_item_dict[order] = [
                    {
                        "name": name,
                        "product_id": product_dict[product_id_value],
                        "product_uom_qty": qty,
                        "product_uom": product_data.uom_id.id,
                        "price_unit": price_unit_value,
                        "state": state,
                        "tax_id": taxes,
                        "invoiceable": invoiceable,
                    }
                ]
            else:
                order_item_dict[order].append(
                    {
                        "name": name,
                        "product_id": product_dict[product_id_value],
                        "product_uom_qty": qty,
                        "product_uom": product_data.uom_id.id,
                        "price_unit": price_unit_value,
                        "state": state,
                        "tax_id": taxes,
                        "invoiceable": invoiceable,
                    }
                )

    @api.model
    def _get_order_dict(
        self,
        data_import_log_id,
        order_dict,
        order,
        partner_dict,
        partner_value,
        pricelist_dict,
        pricelist_value,
        picking_dict,
        picking_policy,
        team_dict,
        team_value,
        carrier_dict,
        carrier_value,
        warehouse_dict,
        warehouse_value,
        notes,
    ):
        """Get order dict"""
        if not data_import_log_id:
            if order not in order_dict:
                partner_data = self.env["res.partner"].browse(
                    partner_dict[partner_value]
                )
                addr = partner_data.address_get(["delivery", "invoice"])
                order_dict[order] = {
                    "partner_id": partner_dict[partner_value],
                    "partner_invoice_id": addr["invoice"],
                    "pricelist_id": pricelist_dict[pricelist_value],
                    "location_id": picking_dict[
                        warehouse_value
                    ].default_location_dest_id
                    and picking_dict[warehouse_value].default_location_dest_id.id,
                    "partner_shipping_id": addr["delivery"],
                    "payment_term": partner_data.property_payment_term_id
                    and partner_data.property_payment_term_id.id
                    or False,
                    "picking_policy": picking_policy,
                    "team_id": team_dict[team_value],
                    "carrier_id": carrier_dict[carrier_value]
                    if carrier_value
                    else False,
                    "warehouse_id": warehouse_dict[warehouse_value],
                    "note": notes,
                }

    @api.model
    def _get_partner_dict(self, partner_value, partner_dict):
        if partner_value not in partner_dict.keys():
            Partner = self.env["res.partner"]
            partner = Partner.search(
                [
                    "|",
                    ("phone", "=", partner_value),
                    ("mobile", "=", partner_value),
                ]
            )
            if not partner:
                partner_name = self._context.get("partner_name", False)
                partner_id = Partner.create(
                    {
                        "name": partner_name or partner_value,
                        "phone": partner_value,
                        "mobile": partner_value,
                    }
                )
                partner_dict[partner_value] = partner_id.id
            else:
                #  pick the first partner that matches the domain
                #  fixme logic should be further refined
                partner_dict[partner_value] = partner[0].id

    @api.model
    def _get_product_dict(self, product_id_value, product_dict, error_vals):
        if product_id_value not in product_dict.keys():
            product_product = self.env["product.product"]
            product = product_product.search([("default_code", "=", product_id_value)])
            if not product:
                error_vals["error_message"] = (
                    error_vals["error_message"]
                    + _("Product: ")
                    + product_id_value
                    + _(" not found!")
                    + "\n"
                )
                error_vals["error"] = True
            else:
                product_dict[product_id_value] = product.id

    @api.model
    def _get_pricelist_dict(self, pricelist_value, pricelist_dict, error_vals):
        if pricelist_value not in pricelist_dict.keys():
            product_pricelist = self.env["product.pricelist"]
            pricelist = product_pricelist.search([("name", "=", pricelist_value)])
            if not pricelist:
                error_vals["error_message"] = (
                    error_vals["error_message"]
                    + _("Pricelist: ")
                    + pricelist_value
                    + _(" not found!")
                    + "\n"
                )
                error_vals["error"] = True
            else:
                pricelist_dict[pricelist_value] = pricelist.id

    @api.model
    def _get_picking_dict(
        self, warehouse_value, picking_dict, warehouse_dict, error_vals
    ):
        stock_warehouse = self.env["stock.warehouse"]
        warehouse_id = stock_warehouse.search([("name", "=", warehouse_value)]).id
        if not warehouse_id:
            error_vals["error_message"] = (
                error_vals["error_message"]
                + _("Warehouse: ")
                + warehouse_value
                + _(" not found!")
                + "\n"
            )
            error_vals["error"] = True
        else:
            stock_picking_type = self.env["stock.picking.type"]
            picking_type = stock_picking_type.search(
                [("warehouse_id", "=", warehouse_id), ("code", "=", "outgoing")]
            )
            picking_dict[warehouse_value] = picking_type
            warehouse_dict[warehouse_value] = warehouse_id

    @api.model
    def _get_carrier_dict(self, carrier_value, carrier_dict, error_vals):
        carrier_obj = self.env["delivery.carrier"]
        carrier_id = carrier_obj.search([("name", "=", carrier_value)])
        if not carrier_id:
            error_vals["error_message"] = (
                error_vals["error_message"]
                + _("Carrier: ")
                + carrier_value
                + _(" not found!")
                + "\n"
            )
            error_vals["error"] = True
        else:
            # pick the first carrier that matches the domain
            carrier_dict[carrier_value] = carrier_id[0].id

    @api.model
    def _get_team_dict(self, team_value, team_dict, error_vals):
        crm_team = self.env["crm.team"]
        team_id = crm_team.search([("name", "=", team_value)])
        if not team_id:
            error_vals["error_message"] = (
                error_vals["error_message"]
                + _("Team: ")
                + team_value
                + _(" not found!")
                + "\n"
            )
            error_vals["error"] = True
        else:
            # pick the first team that matches the domain
            team_dict[team_value] = team_id[0].id

    @api.model
    def _get_taxes(self, tax_from_chunk, taxes, error_vals):
        tax_name_list = tax_from_chunk.split(",")
        for tax_name in tax_name_list:
            tax = self.env["account.tax"].search([("name", "=", tax_name)], limit=1)
            if not tax:
                error_vals["error_message"] = (
                    error_vals["error_message"]
                    + _("Tax: ")
                    + tax_name
                    + _(" not found!")
                    + "\n"
                )
                error_vals["error"] = True
            else:
                for taxdata in tax:
                    taxes.append(taxdata.id)

    @api.model
    def _update_data_import_log(
        self,
        data_import_log_id,
        error_vals,
        ir_attachment,
        model,
        row_no,
        order_group_value,
    ):
        """Update data import log"""
        error_line = self.env["data.import.error"]
        if not data_import_log_id and error_vals["error"]:
            data_import_log = self.env["data.import.log"]
            data_import_log_id = data_import_log.create(
                {
                    "input_file": ir_attachment.id,
                    "import_user_id": self.env.user.id,
                    "import_date": datetime.now(),
                    "state": "failed",
                    "model_id": model.id,
                }
            ).id
            error_line.create(
                {
                    "row_no": row_no,
                    "reference": order_group_value,
                    "error_message": error_vals["error_message"],
                    "log_id": data_import_log_id,
                }
            )
        elif error_vals["error"]:
            error_line.create(
                {
                    "row_no": row_no,
                    "reference": order_group_value,
                    "error_message": error_vals["error_message"],
                    "log_id": data_import_log_id,
                }
            )
        return data_import_log_id

    def import_sale_data(self):
        self.ensure_one()
        ctx = self._context.copy()
        model = self.env["ir.model"].search([("model", "=", "sale.order")])

        product_dict = {}
        partner_dict = {}
        pricelist_dict = {}
        order_item_dict = {}
        order_dict = {}
        picking_dict = {}
        warehouse_dict = {}
        team_dict = {}
        carrier_dict = {}
        data_import_log_id = False
        ir_attachment_obj = self.env["ir.attachment"]
        ir_attachment = ir_attachment_obj.create(
            {
                "name": self.datas_fname,
                "datas": self.input_file,
            }
        )

        csv_data = base64.decodebytes(self.input_file)
        csv_iterator = pycompat.csv_reader(
            io.BytesIO(csv_data), quotechar='"', delimiter=","
        )
        try:
            sheet_fields = next(csv_iterator)
        except Exception:
            raise UserError(
                _("Please import a CSV file with UTF-8 encoding.")
            ) from None

        #  column validation
        missing_columns = list(set(FIELDS_TO_IMPORT) - set(sheet_fields))
        if missing_columns:
            raise ValidationError(
                _("Following columns are missing: \n %s") % "\n".join(missing_columns)
            )

        field_defs = self._get_field_defs(FIELD_KEYS, FIELD_VALS)
        for row in csv_iterator:
            row_dict, error_list = self._check_field_vals(field_defs, row, sheet_fields)
            order_group = row_dict.get("order_group")
            partner_name = row_dict.get("partner_name")
            partner_tel = row_dict.get("partner_tel")
            product_id = row_dict.get("product_id")
            line_name = row_dict.get("line_name")
            price_unit = row_dict.get("price_unit")
            product_qty = row_dict.get("product_qty")
            taxes_id = row_dict.get("taxes_id")
            notes = row_dict.get("notes")
            pricelist_id = row_dict.get("pricelist_id")
            warehouse_id = row_dict.get("warehouse_id")
            team_id = row_dict.get("team_id")
            carrier_id = row_dict.get("carrier_id")
            error_vals = {"error_message": "", "error": False}
            check_list = []
            # if row values are empty in all columns then skip that line.
            if not bool(order_group):
                for r in row:
                    if bool(r.strip()):
                        check_list.append(r)
                if not check_list:
                    continue
            order = order_group
            if error_list:
                error_vals["error_message"] = "\n".join(error_list)
                error_vals["error"] = True
                data_import_log_id = self._update_data_import_log(
                    data_import_log_id,
                    error_vals,
                    ir_attachment,
                    model,
                    csv_iterator.line_num,
                    order,
                )
                continue

            ctx.update({"partner_name": partner_name})
            (
                partner_value,
                product_id_value,
                pricelist_value,
                warehouse_value,
                team_value,
                carrier_value,
            ) = self.with_context(**ctx)._get_order_value_dict(
                error_vals,
                partner_tel,
                product_id,
                pricelist_id,
                warehouse_id,
                team_id,
                carrier_id,
                partner_dict,
                product_dict,
                pricelist_dict,
                picking_dict,
                warehouse_dict,
                team_dict,
                carrier_dict,
            )

            taxes = []
            qty, price_unit_value = self._get_order_value(
                error_vals, taxes, taxes_id, price_unit, product_qty
            )
            picking_policy = self.picking_policy
            data_import_log_id = self._update_data_import_log(
                data_import_log_id,
                error_vals,
                ir_attachment,
                model,
                csv_iterator.line_num,
                order,
            )

            self._get_order_item_dict(
                data_import_log_id,
                order,
                taxes,
                line_name,
                product_dict,
                product_id_value,
                order_item_dict,
                qty,
                price_unit_value,
            )

            self._get_order_dict(
                data_import_log_id,
                order_dict,
                order,
                partner_dict,
                partner_value,
                pricelist_dict,
                pricelist_value,
                picking_dict,
                picking_policy,
                team_dict,
                team_value,
                carrier_dict,
                carrier_value,
                warehouse_dict,
                warehouse_value,
                notes,
            )

        if not data_import_log_id:
            data_import_log_id = (
                self.env["data.import.log"]
                .create(
                    {
                        "input_file": ir_attachment.id,
                        "import_user_id": self.env.user.id,
                        "import_date": datetime.now(),
                        "state": "done",
                        "model_id": model.id,
                    }
                )
                .id
            )
            payment_journal = False
            if self.process_payment:
                payment_journal = self.customer_payment_journal_id
            for item in order_item_dict:
                self_delay = self
                if self.asynchronous:
                    self_delay = self.with_delay()
                self_delay._process_order(
                    order_dict[item],
                    order_item_dict[item],
                    item,
                    data_import_log_id,
                    self.customer_invoice_journal_id,
                    payment_journal,
                )

        res = self.env.ref("base_data_import.data_import_log_action")
        res = res.read()[0]
        res["domain"] = str([("id", "in", [data_import_log_id])])
        return res

    @api.model
    def _process_order(
        self,
        order_data,
        line_data,
        item,
        data_import_log_id,
        invoice_journal,
        payment_journal,
    ):
        order = self._create_order(order_data, item, data_import_log_id)
        for line in line_data:
            if not line["invoiceable"]:
                order.invoiceable = False
            self._create_order_line(line, order)
        order.action_confirm()
        if order.picking_ids:
            for picking in order.picking_ids:
                picking.action_assign()
        if order.invoiceable:
            order._create_invoices()
        if order.invoice_ids:
            for invoice in order.invoice_ids:
                invoice.journal_id = invoice_journal.id
                if invoice.state == "draft":
                    invoice.action_post()
                if payment_journal:
                    self.env["account.payment.register"].with_context(
                        active_model="account.move", active_ids=invoice.ids
                    ).create({"journal_id": payment_journal.id})._create_payments()

    @api.model
    def _create_order(self, order_data, item, data_import_log_id):
        order_vals = {
            "partner_id": order_data["partner_id"],
            "partner_invoice_id": order_data["partner_invoice_id"],
            "pricelist_id": order_data["pricelist_id"],
            "partner_shipping_id": order_data["partner_shipping_id"],
            "payment_term_id": order_data["payment_term"],
            "state": "draft",
            "picking_policy": order_data["picking_policy"],
            "note": order_data["note"],
            "data_import_log_id": data_import_log_id,
            "imported_order": True,
            "order_ref": item,
            "team_id": order_data["team_id"],
            "warehouse_id": order_data["warehouse_id"],
            "carrier_id": order_data["carrier_id"],
        }
        return self.env["sale.order"].create(order_vals)

    @api.model
    def _create_order_line(self, line, order):
        line_vals = {
            "name": line["name"],
            "product_id": line["product_id"],
            "product_uom_qty": line["product_uom_qty"],
            "product_uom": line["product_uom"],
            "price_unit": line["price_unit"],
            "state": line["state"],
            "tax_id": [(6, 0, line["tax_id"])],
            "order_id": order.id,
        }
        return self.env["sale.order.line"].create(line_vals)
