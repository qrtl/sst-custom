# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    penalty_product_id = fields.Many2one(
        'product.product',
        string='Cart Product Removal Penalty'
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(penalty_product_id = int(get_param(
            'website_sale_remove_product_penalty.penalty_product_id',
            default=False)))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('website_sale_remove_product_penalty.penalty_product_id',
                  self.penalty_product_id.id)
