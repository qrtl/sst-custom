# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def update_data_sync(self, data=None):
        update_product_dict = {}
        for product_data in data:
            if product_data == 'create':
                product_id = self.create(
                    data[product_data]
                )
                update_product_dict.update({str(product_id.id):data[product_data]})
            else:
                product_id = self.env['product.product'].browse(int(product_data))
                product_id.write(data[product_data])
                update_product_dict.update({str(product_id.id):data[product_data]})
        
        return update_product_dict

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
