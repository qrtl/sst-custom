# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, vals):
        if "product_id" in vals:
            product = self.env["product.product"].browse(vals["product_id"])
            product.in_cart = True
        return super(
            SaleOrderLine,
            self,
        ).create(vals)

    @api.multi
    def write(self, vals):
        if "product_id" in vals:
            for order_line in self:
                if order_line.team_id.team_type == "website":
                    order_line.product_id.in_cart = False
        res = super(SaleOrderLine, self).write(vals)
        if "product_id" in vals:
            for order_line in self:
                if order_line.team_id.team_type == "website":
                    order_line.product_id.in_cart = True
        return res

    @api.multi
    def unlink(self):
        for order_line in self:
            order_line.product_id.in_cart = False
        return super(SaleOrderLine, self).unlink()
