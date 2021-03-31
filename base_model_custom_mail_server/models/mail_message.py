# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    # Override the reply-to address since Amazon SES requires a verified reply-to address # noqa
    @api.model
    def _get_reply_to(self, values):
        res = super(MailMessage, self)._get_reply_to(values)
        if "model" in values:
            message_model = (
                self.env["ir.model"].sudo().search([("model", "=", values["model"])])
            )
            if (
                message_model.use_custom_mail_server
                and message_model.custom_mail_server_id
            ):
                return "<%s>" % message_model.custom_mail_server_id.smtp_from
        return res
