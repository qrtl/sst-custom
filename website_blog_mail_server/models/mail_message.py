# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _get_reply_to(self, values):
        res = super(MailMessage, self)._get_reply_to(values)
        if 'model' in values:
            print(values['model'])
        if 'model' in values and values['model'] in ('blog.blog', 'blog.post'):
            website_blog_mail_server_id = self.env['website'].sudo().get_current_website().website_blog_mail_server_id
            if website_blog_mail_server_id and website_blog_mail_server_id.smtp_from:
                return "<%s>" % website_blog_mail_server_id.smtp_from
        return res
