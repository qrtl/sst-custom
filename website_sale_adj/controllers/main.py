# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    # Avoid this issue: https://github.com/odoo/odoo/issues/35399
    # Triggering sale_get_order() in confirmation page so that a new quotation
    # will be created after the checkout. Hence "Add to Cart" requests will 
    # not cause the server creating multiple quotations.
    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        res = super(WebsiteSale, self).payment_confirmation(**post)
        request.website.sale_get_order(force_create=True)
        return res
