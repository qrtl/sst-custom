# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    # Overwrite _get_search_order() so the product will be sorted by
    # website_sequence_date in the website
    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        # return 'website_published desc,%s , id desc' % post.get('order', 'website_sequence desc')
        return 'website_published desc, website_sequence_date desc, id desc'
