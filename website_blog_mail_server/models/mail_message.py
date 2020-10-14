# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _get_reply_to(self, values):
        res = super(MailMessage, self)._get_reply_to(values)
        if 'model' in values and values['model'] in ('blog.blog', 'blog.post'):
            blog_mail_server_id = self.env['website'].sudo().get_current_website().blog_mail_server_id
            if blog_mail_server_id and blog_mail_server_id.smtp_from:
                return "<%s>" % blog_mail_server_id.smtp_from
        return res
