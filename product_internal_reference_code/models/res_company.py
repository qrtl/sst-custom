# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.multi
    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        # Create the sequence for the company upon creation
        seq = {
            "name": res.name + " - Product Sequence",
            "code": "product.product.internal_code",
            "prefix": res.id,
            "padding": 5,
            "number_increment": 1,
            "company_id": res.id,
        }
        self.env["ir.sequence"].create(seq)
        return res
