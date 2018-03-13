# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.http import request


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _notify(self, message, force_send=False, send_after_commit=True,
                user_signature=True):
        if message.model == 'product.template' and request and \
                request.httprequest:
            message.product_url = request.httprequest.referrer
        res = super(ResPartner, self)._notify(
            message=message,
            force_send=force_send,
            send_after_commit=send_after_commit,
            user_signature=user_signature
        )
        return res
