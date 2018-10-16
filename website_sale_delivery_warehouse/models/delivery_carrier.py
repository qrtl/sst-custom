# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_warehouse_id = fields.Many2one(
        'stock.warehouse',
        'Delivery Warehouse'
    )
