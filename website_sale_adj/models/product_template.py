# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_sequence_date = fields.Datetime(
        string="Website Sequence Date", default=fields.Datetime.now,
    )

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if vals.get("website_published") or vals.get("list_price"):
            for product in self:
                if product.website_published:
                    product.website_sequence_date = fields.Datetime.now()
        return res

    @api.multi
    def _update_website_sequence_date(self):
        return self.update({"website_sequence_date": fields.Datetime.now()})
