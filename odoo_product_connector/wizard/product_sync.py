# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

from odoo.exceptions import ValidationError

class ProductSync(models.TransientModel):
    _name = "product.sync"

    @api.multi
    def action_product_sync(self):
        product_ids = self.env['product.product'].browse(self._context.get("active_ids"))
        company_id = self.env.user.company_id
        if not (company_id.db_name and company_id.host_name and company_id.user_name and company_id.password):
            raise ValidationError("Please Configure Databse Setting")
        product_sync_dict = {}
        for product in product_ids:
            sync_history_ids = product.sync_history_ids.filtered(lambda sync_history: sync_history.is_sync == False)
            if product.ext_sync_product_id and sync_history_ids:
                sync_history_dict = {'product_id': product.id,'sync_ids': sync_history_ids.ids,}
                for sync_history_id in sync_history_ids:
                    sync_history_dict.update({
                        sync_history_id.field_name: sync_history_id.field_value,
                    })
                product_sync_dict.update({str(product.ext_sync_product_id):sync_history_dict})
            elif not product.ext_sync_product_id:
                product_sync_dict.update({
                    'create' : {
                        'product_id': product.id,
                        'name': product.name,
                        'default_code': product.default_code,
                        'type': product.type,
                        'categ_id': product.categ_id.id,
                        'uom_id': product.uom_id.id,
                        'uom_po_id': product.uom_po_id.id,
                        'lst_price': product.lst_price,
                        'standard_price': product.standard_price,
                    }
                })

            if product_sync_dict:
                product_model = self.env['product.product']
                description = "Update data from Source Databse of product.product %s Database to destination Database in product.product"%(product)
                product_model.with_delay(description=description).product_sync(product_sync_dict)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
