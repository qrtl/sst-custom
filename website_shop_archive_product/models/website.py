# -*- coding: utf-8 -*-


from odoo import api, fields, models, tools
from odoo.http import request

class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def sale_product_domain(self):
        if request.session.get('product_archive'):
            domain = [("sale_ok", "=", True),'|',  ('active', '=', False),('active', '=', True)]
        else:
            domain = [("sale_ok", "=", True)]
        return domain
