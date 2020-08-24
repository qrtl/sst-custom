# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http

from odoo.addons.website_sale_options.controllers.main import WebsiteSaleOptions


class WebsiteSale(WebsiteSaleOptions):
    @http.route(
        [
            "/shop",
            "/shop/page/<int:page>",
            '/shop/category/<model("product.public.category"):category>',
            "/shop/category/<model("
            '"product.public.category"):category>/page/<int:page>',
        ],
        type="http",
        auth="user",
        website=True,
    )
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        return super(WebsiteSale, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post
        )

    @http.route(
        ['/shop/product/<model("product.template"):product>'],
        type="http",
        auth="user",
        website=True,
    )
    def product(self, product, category="", search="", **kwargs):
        return super(WebsiteSale, self).product(
            product=product, category=category, search=search, **kwargs
        )

    @http.route(["/shop/cart"], type="http", auth="user", website=True)
    def cart(self, access_token=None, revive="", **post):
        return super(WebsiteSale, self).cart(
            access_token=access_token, revive=revive, **post
        )
