# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    db_name = fields.Char(
        "Database Name",
    )
    password = fields.Char(
        'Password',
        size=40
    )
    user_name = fields.Char(
        'User Name',
    )
    host_name = fields.Char(
        'Host Name',
    )
