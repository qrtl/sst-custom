# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    employee_id = fields.Many2one("hr.employee", "Received By")
    address = fields.Char()
    remark = fields.Text("Remark")
    worked_hours = fields.Selection(
        [
            (num, num + " hours")
            for num in [
                "0.5",
                "1.0",
                "1.5",
                "2.0",
                "2.5",
                "3.0",
                "3.5",
                "4.0",
                "4.5",
                "5.0",
                "5.5",
                "6.0",
                "6.5",
                "7.0",
                "7.5",
                "8.0",
                "8.5",
                "9.0",
                "9.5",
                "10.0",
            ]
        ],
        string="Worked Hours",
    )
    date_planned = fields.Datetime(
        compute=False,
    )
    sale_prediction_amount = fields.Monetary("Sales Prediction")

    @api.multi
    def open_record(self):
        form_id = self.env.ref("purchase.purchase_order_form")
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "res_id": self.id,
            "view_type": "form",
            "view_mode": "form",
            "view_id": form_id.id,
            "context": {},
            "target": "current",
        }

    @api.multi
    def button_confirm(self):
        for purchase_order in self:
            if self.is_default_partner(purchase_order.partner_id.id):
                raise UserError(
                    _("Purchase order cannot be confirmed with " "default guest user.")
                )
            if not purchase_order.date_planned:
                purchase_order.date_planned = fields.Datetime.now()
                for order_line in purchase_order.order_line:
                    order_line.date_planned = purchase_order.date_planned
        return super(PurchaseOrder, self).button_confirm()

    def is_default_partner(self, partner_id):
        company_id = self.env.user.company_id.id
        default_id = (
            self.env["ir.default"].get(
                "purchase.order",
                "partner_id",
                user_id=self.env.uid,
                company_id=company_id,
            )
            or self.env["ir.default"].get(
                "purchase.order", "partner_id", user_id=False, company_id=company_id
            )
            or False
        )
        return partner_id == default_id

    @api.onchange("date_planned")
    def onchange_date_planned(self):
        if self.date_planned:
            for order_line in self.order_line:
                order_line.date_planned = self.date_planned
