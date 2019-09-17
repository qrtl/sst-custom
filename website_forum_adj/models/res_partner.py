# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _notify_prepare_email_values(self, message):
        mail_values = super(
            ResPartner, self)._notify_prepare_email_values(message)
        if message.model and message.model == 'forum.post':
            forum_mail_server_id = self.env['website'].sudo(
            ).get_current_website().forum_mail_server_id
            if forum_mail_server_id:
                mail_values['mail_server_id'] = forum_mail_server_id.id
        return mail_values
