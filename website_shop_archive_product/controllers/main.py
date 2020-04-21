# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route("/shop/active", type="http", auth="public", website=True)
    def shop_active(self):
        request.session.update({"product_archive": True})
        return request.redirect("/shop")

    @http.route("/shop/in_active", type="http", auth="public", website=True)
    def shop_in_active(self):
        request.session.update({"product_archive": False})
        return request.redirect("/shop")
