# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _notify_prepare_email_values(self, message):
        mail_values = super(ResPartner, self)._notify_prepare_email_values(message)
        message_model = self.env['ir.model'].sudo().search([('model', '=', message.model)])
        if message_model.use_custom_mail_server and message_model.custom_mail_server_id:
            mail_values["mail_server_id"] = message_model.custom_mail_server_id.id
        return mail_values
