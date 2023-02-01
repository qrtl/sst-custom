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
                line.delivered_amount = line.price_total
                continue
            qty_delivered = sum(line.sale_line_ids.mapped("qty_delivered"))
            if qty_delivered > 0:
                line.is_delivered = True
                currency = line.invoice_id and line.invoice_id.currency_id or None
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = False
                if line.invoice_line_tax_ids:
                    taxes = line.invoice_line_tax_ids.compute_all(
                        price,
                        currency,
                        qty_delivered,
                        product=line.product_id,
                        partner=line.invoice_id.partner_id,
                    )
                delivered_subtotal = (
                    taxes["total_excluded"] if taxes else qty_delivered * price
                )
                line.delivered_amount = (
                    taxes["total_included"] if taxes else delivered_subtotal
                )
