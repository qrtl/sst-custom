# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    team_ids = fields.Many2many(
        "crm.team",
        "product_tmpl_team_rel",
        "product_tmpl_id",
        "team_id",
        "Sales Channels",
    )
    manufacturer = fields.Char()
    manufactured_year = fields.Selection(
        [(num, str(num)) for num in reversed(range(1900, datetime.now().year + 1))],
    )
    model = fields.Char()
    evaluated_by_id = fields.Many2one("hr.employee")
    purchased_by_id = fields.Many2one("hr.employee")
    shop_id = fields.Many2one("stock.warehouse", string="Shop Purchased")
    list_price = fields.Float(track_visibility="onchange")
