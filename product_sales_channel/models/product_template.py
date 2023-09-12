# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

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
