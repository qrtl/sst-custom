# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    forum_mail_server_id = fields.Many2one(
        "ir.mail_server",
        related="website_id.forum_mail_server_id",
        string="Mail Server for Forum's Updates",
    )
