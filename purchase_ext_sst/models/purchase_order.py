# Copyright 2017-2023 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    employee_id = fields.Many2one("hr.employee", "Received By")
    address = fields.Char()
    remark = fields.Text()
    date_planned = fields.Datetime(compute=False)
    sale_prediction_amount = fields.Monetary("Sales Prediction")

    @api.multi
    def button_confirm(self):
        for order in self:
            if self.is_default_partner(order.partner_id.id):
                raise UserError(
                    _("Purchase order cannot be confirmed with default guest user.")
                )
            if not order.date_planned:
                order.date_planned = fields.Datetime.now()
                for order_line in order.order_line:
                    order_line.date_planned = order.date_planned
        return super(PurchaseOrder, self).button_confirm()

    def is_default_partner(self, partner_id):
        company = self.env.user.company_id
        default_id = (
            self.env["ir.default"].get(
                "purchase.order",
                "partner_id",
                user_id=self.env.uid,
                company_id=company.id,
            )
            or self.env["ir.default"].get(
                "purchase.order", "partner_id", user_id=False, company_id=company.id
            )
            or False
        )
        return partner_id == default_id

    @api.onchange("date_planned")
    def onchange_date_planned(self):
        if self.date_planned:
            for line in self.order_line:
                line.date_planned = self.date_planned
