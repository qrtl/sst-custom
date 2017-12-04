# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class YahooProductState(models.Model):
    _name = 'yahoo.product.state'

    status = fields.Char(
        string='Status',
        require=True,
    )

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.status))
        return res
