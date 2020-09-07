# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sale_price_unit = fields.Monetary(
        string="Sale Price (Actual)",
        digits=dp.get_precision("Product Price"),
        readonly=True,
        store=True,
    )
    gross_profit = fields.Monetary(
        string="Gross Profit",
        digits=dp.get_precision("Product Price"),
        compute="_compute_gross_profit",
        readonly=True,
        store=True,
    )
    confirmation_date = fields.Datetime(string="Confirmation Date", readonly=True,)
    team_id = fields.Many2one("crm.team", string="Sales Channel", readonly=True,)

    @api.depends("sale_price_unit", "list_price", "standard_price")
    def _compute_gross_profit(self):
        for pt in self:
            if pt.sales_count:
                pt.gross_profit = pt.sale_price_unit - pt.standard_price
            else:
                pt.gross_profit = pt.list_price - pt.standard_price

    @api.multi
    def _update_sale_price_unit(self):
        for pt in self:
            invoice_line = self.env["account.invoice.line"].search(
                [
                    ("product_id.product_tmpl_id", "=", pt.id),
                    ("invoice_type", "=", "out_invoice"),
                    ("invoice_id.state", "in", ("open", "paid")),
                ],
                limit=1,
            )
            if invoice_line:
                pt.sale_price_unit = invoice_line.price_total / invoice_line.quantity
            else:
                order_line = self.env["sale.order.line"].search(
                    [
                        ("product_id.product_tmpl_id", "=", pt.id),
                        ("state", "in", ("confirm", "done")),
                    ],
                    limit=1,
                )
                if order_line:
                    pt.sale_price_unit = order_line.price_reduce_taxinc
