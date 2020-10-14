# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    blog_mail_server_id = fields.Many2one(
        "ir.mail_server", string="Mail Server for Blog's Updates",
    )
