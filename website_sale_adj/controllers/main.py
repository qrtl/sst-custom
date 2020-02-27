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

    # Overwrite _get_search_order() so the product will be sorted by
    # website_sequence_date in the website
    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        # return 'website_published desc,%s , id desc' % post.get('order', 'website_sequence desc')
        return 'website_published desc, website_sequence_date desc, id desc'
