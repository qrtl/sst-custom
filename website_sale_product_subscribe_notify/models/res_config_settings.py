# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    email_recipient_limit = fields.Integer(string="Number of Recipients Per Email")

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.default"].sudo().set(
            "res.config.settings", "email_recipient_limit", self.email_recipient_limit
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        email_recipient_limit = self.env["ir.default"].get(
            "res.config.settings", "email_recipient_limit"
        )
        res.update(email_recipient_limit=email_recipient_limit,)
        return res

    @api.constrains("email_recipient_limit")
    def _check_email_recipient_limit(self):
        if self.email_recipient_limit <= 0:
            raise ValidationError(
                _("Limit Email Recipient should be greater " "than 0.")
            )
