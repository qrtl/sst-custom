# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _notify(self, message, force_send=False, send_after_commit=True,
                user_signature=True):
        if message.model == 'product.template':
            product = self.env['product.template'].browse(message.res_id)
            if product:
                base_url = self.env['ir.config_parameter'].sudo().get_param(
                    'web.base.url')
                message.product_url = base_url + product.website_url
        res = super(ResPartner, self)._notify(
            message=message,
            force_send=force_send,
            send_after_commit=send_after_commit,
            user_signature=user_signature
        )
        return res
