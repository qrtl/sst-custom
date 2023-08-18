# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_category_id = fields.Many2one(
        "purchase.category",
        "Purchase Category",
    )
