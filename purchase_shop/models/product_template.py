# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    shop_id = fields.Many2one("stock.warehouse", string="Shop Purchased")
    evaluated_by_id = fields.Many2one("hr.employee")
    purchased_by_id = fields.Many2one("hr.employee")
