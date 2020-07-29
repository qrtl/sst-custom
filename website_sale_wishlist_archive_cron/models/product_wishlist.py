# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductWishlist(models.Model):
    _inherit = "product.wishlist"

    @api.model
    def _process_wishlist_archive(self):
        wishlist_records = self.search([("active", "=", True)])
        for record in wishlist_records:
            if not record.product_id.active:
                record.active = False
