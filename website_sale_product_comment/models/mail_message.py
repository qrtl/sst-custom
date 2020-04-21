# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    product_url = fields.Char()
