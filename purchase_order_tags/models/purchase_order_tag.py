# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PurchaseOrderTag(models.Model):
    _name = "purchase.order.tag"

    name = fields.Char(required=True, translate=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the tag without removing it.",
    )
