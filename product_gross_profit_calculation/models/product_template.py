# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sale_price_unit = fields.Float(
        string="Sale Price (Actual)",
        digits="Product Price",
        readonly=True,
        store=True,
    )
    gross_profit = fields.Float(
        digits="Product Price",
        compute="_compute_gross_profit",
        readonly=True,
        store=True,
    )
    confirmation_date = fields.Datetime(
        readonly=True,
    )
    team_id = fields.Many2one(
        "crm.team",
        string="Sales Channel",
        readonly=True,
    )

    @api.depends("sale_price_unit", "list_price", "standard_price")
    def _compute_gross_profit(self):
        for template in self:
            if template.sales_count:
                template.gross_profit = (
                    template.sale_price_unit - template.standard_price
                )
            else:
                template.gross_profit = template.list_price - template.standard_price
