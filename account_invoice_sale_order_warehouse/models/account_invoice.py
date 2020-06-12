# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    sale_order_warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Sale Order Warehouse",
        compute="_compute_sale_order_warehouse_id",
    )

    @api.multi
    def _compute_sale_order_warehouse_id(self):
        for invoice in self:
            order = invoice.invoice_line_ids.mapped("sale_line_ids").mapped("order_id")
            if order:
                invoice.sale_order_warehouse_id = order[0].warehouse_id
