# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    smtp_from = fields.Char(
        string="Email From", help="Set this in order to email from a specific address."
    )

    @api.model
    def send_email(
        self,
        message,
        mail_server_id=None,
        smtp_server=None,
        smtp_port=None,
        smtp_user=None,
        smtp_password=None,
        smtp_encryption=None,
        smtp_debug=False,
        smtp_session=None,
    ):
        mail_server = None
        if mail_server_id:
            mail_server = self.sudo().browse(mail_server_id)
        elif not smtp_server:
            mail_server = self.sudo().search([], order="sequence", limit=1)

        if mail_server and mail_server.smtp_from:
            split_from = message["From"].rsplit(" <", 1)
            if len(split_from) > 1:
                email_from = "{} <{}>".format(split_from[0], mail_server.smtp_from)
            else:
                email_from = mail_server.smtp_from

            message.replace_header("From", email_from)
            bounce_alias = self.env["ir.config_parameter"].get_param(
                "mail.bounce.alias"
            )
            if not bounce_alias:
                # then, bounce handling is disabled and we want
                # Return-Path = From
                if "Return-Path" in message:
                    message.replace_header("Return-Path", email_from)
                else:
                    message.add_header("Return-Path", email_from)

        return super(IrMailServer, self).send_email(
            message,
            mail_server_id=mail_server_id,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            smtp_encryption=smtp_encryption,
            smtp_debug=smtp_debug,
            smtp_session=smtp_session,
        )
