# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from ast import literal_eval

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_country_id = fields.Many2one(
        'res.country',
        string='Default Country',
        help='Assign the default country to website address templates.',
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        default_country_id = literal_eval(get_param('l10n_jp_address_layout_website_sale.default_country_id', default='False'))
        if default_country_id and not self.env['res.country'].sudo().browse(
                default_country_id).exists():
            default_country_id = False
        res.update(
            default_country_id=default_country_id
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'l10n_jp_address_layout_website_sale.default_country_id',
            repr(self.default_country_id.id))
