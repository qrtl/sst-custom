# -*- coding: utf-8 -*-

from odoo import models, fields

class Company(models.Model):
    _inherit = "res.company"
    
    internal_code_prefix = fields.Char(
        string='Internal Reference Prefix',
        copy=False,
    )