# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import request
from odoo.tools.pycompat import izip

from odoo.addons.website_sale_stock.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    # Add website_sale_available_qty to the return value of
    # get_attribute_value_ids that the value will be retrieved by js
    # i.e. https://github.com/odoo/odoo/blob/11.0/addons/website_sale_stock/controllers/main.py#L11-L27 # noqa
    def get_attribute_value_ids(self, product):
        res = super(WebsiteSale, self).get_attribute_value_ids(product)
        variant_ids = [r[0] for r in res]
        for r, variant in izip(
            res, request.env["product.product"].sudo().browse(variant_ids)
        ):
            # Directly refer [4] since 'res' is a list instead of a dict object
            qty = variant.sudo().website_sale_available_qty
            r[4].update({"website_sale_available_qty": qty})
        return res
