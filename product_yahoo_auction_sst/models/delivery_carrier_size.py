# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DeliveryCarrierSize(models.Model):
    _name = "delivery.carrier.size"

    name = fields.Char(string="Size", required=True,)
    carrier_id = fields.Many2one(
        "delivery.carrier", string="Delivery Method", required=True,
    )
