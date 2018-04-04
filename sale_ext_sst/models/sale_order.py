# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    phone = fields.Char(
        related='partner_id.phone',
        string='Phone',
    )
    requested_date = fields.Datetime(
        readonly=False,
    )
