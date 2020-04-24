# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    forum_mail_server_id = fields.Many2one(
        'ir.mail_server',
        related='website_id.forum_mail_server_id',
        string='Mail Server for Forum\'s Updates',
    )
