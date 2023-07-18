# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    delivery_state_id = fields.Many2one('res.country.state', string="Delivery Prefecture", domain="[('is_deliverable','=', True)]")
    delivery_city_id = fields.Many2one('delivery.city', string="Delivery City")

    @api.onchange("delivery_city_id")
    def _onchange_delivery_city_id(self):
        if self.delivery_city_id:
            self.delivery_state_id = self.delivery_city_id.state_id
    
    @api.onchange("delivery_state_id")
    def _onchange_delivery_state_id(self):
        if self.delivery_state_id:
            return {'domain': {'delivery_city_id': [('state_id', '=', self.delivery_state_id.id)]}}
        else:
            return {'domain': {'delivery_city_id': []}}
