# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def sale_product_domain(self):
        if request.session.get("product_archive"):
            domain = [("sale_ok", "=", True), ("active", "=", False)]
        else:
            domain = [("sale_ok", "=", True)]
        return domain
