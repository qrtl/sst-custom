# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class DeliveryCarrierSize(models.Model):
    _name = 'delivery.carrier.size'

    size = fields.Char(
        string = 'Size',
        required = True,
    )
    delivery_method = fields.Many2one(
        'delivery.carrier',
        string = 'Delivery Method',
        required = True,
    )

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.size))
        return res
