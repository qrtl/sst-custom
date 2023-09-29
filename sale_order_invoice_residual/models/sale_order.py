# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # this field is decided to be a non-stored computed field to avoid the
    # complication of the logic and the risk of missing a trigger.
    # reconciling/unreconciling invoice with an existing payment particularly
    # didn't seem to provide the necessary info in context.
    invoice_residual = fields.Monetary(
        "Invoice Amount Due",
        compute="_compute_invoice_residual",
        help="Remaining amount due of invoice(s).",
    )

    def _compute_invoice_residual(self):
        for order in self.filtered(lambda r: r.state in ["sale", "done"]):
            order.invoice_residual = order.amount_total
            if order.invoice_ids:
                # we do not cover refund invoices (origin != order.name) here
                # (it is out of scope)
                order.invoice_residual -= sum(
                    order.invoice_ids.filtered(
                        lambda r: r.origin == order.name and r.state in ["open", "paid"]
                    ).mapped(lambda r: r.amount_total - r.residual)
                )
