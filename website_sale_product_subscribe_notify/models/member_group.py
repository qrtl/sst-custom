# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class MemeberGroup(models.Model):
    _name = 'member.group'

    name = fields.Char(
        string='Group Name',
        required=True,
    )
    point_limit = fields.Integer(
        string='Points Limit',
        required=True,
    )
