# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.mail import PortalChatter


class PortalChatter(PortalChatter):
    @http.route(
        ["/mail/chatter_post"],
        type="http",
        methods=["POST"],
        auth="public",
        website=True,
    )
    def portal_chatter_post(self, res_model, res_id, message, **kw):
        # call super
        res = super(PortalChatter, self).portal_chatter_post(
            res_model=res_model, res_id=res_id, message=message, **kw
        )
        # if comment by public user then call super
        if request.env.user != request.env.ref("base.public_user"):
            # if comment is for only product page
            if res_model and res_model == "product.template":
                if res_id:
                    partner_id = request.env.user.partner_id.id
                    product = request.env[res_model].sudo().browse(int(res_id))
                    if partner_id not in product.message_partner_ids.ids:
                        product.message_subscribe([partner_id])
        return res
