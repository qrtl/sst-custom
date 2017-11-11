# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    identification_type_id = fields.Many2one(
        comodel_name='res.identification.type',
        string='Identification Type',
    )
    identification_number = fields.Char(
        string='Identification Number',
    )
    shop_id = fields.Many2one(
        'stock.warehouse',
        'Shop',
    )
    fax = fields.Char()
    occupation_id = fields.Many2one('res.occupation', 'Occupation')
