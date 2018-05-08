# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductState(models.Model):
    _name = 'product.state'
    _order = 'sequence, name'

    rank = fields.Char('Rank', required=True)
    description = fields.Char('Description', required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'product.state'),
    )

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.rank + "：" + record.description))
        return res
