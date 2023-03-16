# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DeliveryCarrierSize(models.Model):
    _name = "delivery.carrier.size"

    name = fields.Char(
        string="Size",
        required=True,
    )
    carrier_id = fields.Many2one(
        "delivery.carrier",
        string="Delivery Method",
        required=True,
    )
