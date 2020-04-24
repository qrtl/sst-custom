# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Website(models.Model):
    _inherit = 'website'

    forum_mail_server_id = fields.Many2one(
        'ir.mail_server',
        string='Mail Server for Forum\'s Updates',
    )
