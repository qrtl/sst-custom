# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Sale Order Warehouse",
        compute="_compute_warehouse_id",
    )

    @api.multi
    def _compute_warehouse_id(self):
        for invoice in self:
            order = invoice.invoice_line_ids.mapped("sale_line_ids").mapped("order_id")
            if order:
                invoice.warehouse_id = order[0].warehouse_id
