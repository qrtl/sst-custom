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
            # If there is not seq_code, create a new one for the company
            if not seq_code:
                seq = {
                    'name': self.env.user.company_id.name + ' - Product Sequence',
                    'code': 'product.product.internal_code',
                    'prefix': self.env.user.company_id.internal_code_prefix
                              or '',
                    'padding': 5,
                    'number_increment': 1,
                    'company_id': self.env.user.company_id.id
                }
                self.env['ir.sequence'].create(seq)
                seq_code = self.env['ir.sequence'].with_context(
                    force_company=self.env.user.company_id.id).next_by_code(
                    'product.product.internal_code')
            vals.update({'default_code': seq_code})
        return super(ProductProduct, self).create(vals)
