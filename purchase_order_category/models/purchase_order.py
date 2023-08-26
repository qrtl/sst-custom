# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_category_id = fields.Many2one(
        "purchase.category",
        "Purchase Category",
    )

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if "order_line" in vals or "purchase_category_id" in vals:
            for order in self:
                products = order.order_line.mapped("product_id")
                products.write(
                    {"purchase_category_id": order.purchase_category_id.id}
                )
        return res
