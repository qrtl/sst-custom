# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    publish_yahoo_state_id = fields.Many2one(
        'yahoo.product.state',
        string='Yahoo Product State For Published Product',
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(publish_yahoo_state_id = int(get_param(
            'product_yahoo_auction_sst.publish_yahoo_state_id',
            default=False)))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('product_yahoo_auction_sst.publish_yahoo_state_id',
                  self.publish_yahoo_state_id.id)
