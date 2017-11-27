# -*- coding: utf-8 -*-

from odoo import models, fields

class Company(models.Model):
    _inherit = "res.company"
    
    code = fields.Char(
        string='Internal Reference Prefix',
    )
