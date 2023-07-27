# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DeliveryCity(models.Model):
    _name = 'delivery.city'
    _description = 'Delivery City'

    name = fields.Char(string='City Name', required=True)
    state_id = fields.Many2one("res.country.state", required=True, domain="[('is_deliverable','=', True)]")
