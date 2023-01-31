# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    is_delivered = fields.Boolean(
        string="Delivered", compute="_compute_delivered_amount", store=True
    )
    delivered_amount = fields.Monetary(
        string="Delivered Amount", store=True, compute="_compute_delivered_amount"
    )

    @api.depends("quantity", "price_unit", "sale_line_ids.qty_delivered")
    def _compute_delivered_amount(self):
        for line in self:
            if line.product_id.type == "service" or not line.sale_line_ids:
                line.is_delivered = True
                line.delivered_amount = line.quantity * line.price_unit
                continue
            qty_delivered = sum(line.sale_line_ids.mapped("qty_delivered"))
            if qty_delivered > 0:
                line.is_delivered = True
                line.delivered_amount = qty_delivered * line.price_unit
