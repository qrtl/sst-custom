# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModel(models.Model):
    _inherit = "ir.model"

    use_custom_mail_server = fields.Boolean("Custom SMTP Server")
    custom_mail_server_id = fields.Many2one("ir.mail_server", "Outgoing mail server")
