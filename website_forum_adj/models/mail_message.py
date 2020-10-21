# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model
    def _get_reply_to(self, values):
        res = super(MailMessage, self)._get_reply_to(values)
        if "model" in values and values["model"] == "forum.post":
            forum_mail_server = (
                self.env["website"].sudo().get_current_website().forum_mail_server_id
            )
            if forum_mail_server and forum_mail_server.smtp_from:
                return "<%s>" % forum_mail_server.smtp_from
        return res
