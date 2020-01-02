# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_commission_product_id = fields.Many2one(
        'product.product',
        string='Website Sale Commission',
    )
    website_commission_percentage = fields.Float(
        string='Commission Percentage',
        help='Set the percentage to 0 if you want to apply fixed price',
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            website_commission_product_id=int(get_param(
                'website_sale_commission.website_commission_product_id', default=False)),
            website_commission_percentage=float(get_param(
                'website_sale_commission.website_commission_percentage', default=0.0)),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('website_sale_commission.website_commission_product_id',
                  self.website_commission_product_id.id)
        set_param('website_sale_commission.website_commission_percentage',
                  self.website_commission_percentage)
