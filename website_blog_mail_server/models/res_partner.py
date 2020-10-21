# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _notify_prepare_email_values(self, message):
        mail_values = super(ResPartner, self)._notify_prepare_email_values(message)
        if message.model in ("blog.post", "blog.blog"):
            blog_mail_server = (
                self.env["website"].sudo().get_current_website().blog_mail_server_id
            )
            if blog_mail_server:
                mail_values["mail_server_id"] = blog_mail_server.id
        return mail_values
