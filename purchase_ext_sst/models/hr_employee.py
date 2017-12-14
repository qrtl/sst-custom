# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    shop_id = fields.Many2one('stock.warehouse', 'Shop')
