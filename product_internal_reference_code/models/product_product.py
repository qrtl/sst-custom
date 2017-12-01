# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, vals):
        if not vals.get('default_code', False):
            # Get the sequence with user company_id
            seq_code = self.env['ir.sequence'].with_context(
                force_company=self.env.user.company_id.id).next_by_code(
                'product.product.internal_code')
            vals.update({'default_code': seq_code})
        return super(ProductProduct, self).create(vals)
