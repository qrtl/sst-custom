# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Product(models.Model):
    _inherit = "product.product"
    
    @api.model
    def create(self, vals):
        code = self.env.user.company_id.code
        name = self.env['ir.sequence'].next_by_code('product.product.seq')
        new_code = code + name
        vals.update({'default_code': new_code})
        return  super(Product, self).create(vals)