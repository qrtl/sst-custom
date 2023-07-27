# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    delivery_state_id = fields.Many2one('res.country.state', string="Delivery Prefecture", domain="[('is_deliverable','=', True)]")
    delivery_city_id = fields.Many2one('delivery.city', string="Delivery City", domain="[('id', 'in', selectable_delivery_city_ids)]",)
    selectable_delivery_city_ids = fields.Many2many(
        comodel_name="delivery.city", compute="_compute_delivery_city_ids"
    )
    @api.onchange("delivery_city_id")
    def _onchange_delivery_city_id(self):
        if self.delivery_city_id:
            self.delivery_state_id = self.delivery_city_id.state_id
    
    @api.depends("delivery_state_id")
    def _compute_delivery_city_ids(self):
        for rec in self:
            rec.selectable_delivery_city_ids = self.env["delivery.city"].search([('state_id', '=', rec.delivery_state_id.id)])
