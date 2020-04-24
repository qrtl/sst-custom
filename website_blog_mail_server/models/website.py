# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    website_blog_mail_server_id = fields.Many2one(
        'ir.mail_server',
        string='Mail Server for Blog\'s Updates',
    )
