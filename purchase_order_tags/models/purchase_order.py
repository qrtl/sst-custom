# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_tags = fields.Many2many(
        comodel_name="purchase.order.tag", string="Tag(s)", ondelete="restrict"
    )
