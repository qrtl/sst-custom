# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Product(models.Model):
    _inherit = "product.product"
    
    @api.model
    def create(self, vals):
        if not vals.get('default_code', False):
            internal_code_prefix = self.env.user.company_id.internal_code_prefix
            seq_code = self.env['ir.sequence'].next_by_code('product.product.internal_code')
            vals.update({'default_code': internal_code_prefix + seq_code})
        return super(Product, self).create(vals)