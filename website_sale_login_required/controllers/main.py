# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http, tools, _
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="user", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        return super(WebsiteSale, self).shop(page=0, category=None,
                                             search='', ppg=False, **post)

    @http.route([
        '/shop/product/<model("product.template"):product>'],
        type='http', auth="user", website=True)
    def product(self, product, category='', search='', **kwargs):
        return super(WebsiteSale, self).product(product, category='',
                                                search='', **kwargs)

    @http.route(['/shop/cart'], type='http', auth="user", website=True)
    def cart(self, access_token=None, revive='', **post):
        return super(WebsiteSale, self).cart(access_token=None, revive='',
                                             **post)
