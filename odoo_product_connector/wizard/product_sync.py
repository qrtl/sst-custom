# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

from odoo.exceptions import ValidationError

class ProductSync(models.TransientModel):
    _name = "product.sync"

    @api.multi
    def action_product_sync(self):
        active_model = self._context.get("active_model")
        print ("::::::::::activemodel",active_model)
#        product_ids = self.env['product.product'].browse(self._context.get("active_ids"))
        product_ids = self.env[active_model].browse(self._context.get("active_ids"))

        backend_id = self.env['odoo_external.backend'].search([],limit=1)
        if not (backend_id.db_name and backend_id.host_name and backend_id.user_name and backend_id.password):
            raise ValidationError("Please Configure Databse Setting")

        if active_model == 'product.template':
            product_sync_dict = {}

            for product in product_ids:
                variant_ids = product.product_variant_ids.filtered(lambda variant:not variant.ext_sync_product_id)
                variant_lst = []

                for variant in variant_ids:
                    variant_vals = variant.read(['image_medium', 'name', 'default_code', 'type', 'lst_price', 'standard_price'])
                    variant_vals[0].update({'external_product_id':variant_vals[0].get("id")})
                    variant_vals[0]['image_medium'] = (variant_vals[0]['image_medium']).decode("utf-8")
                    variant_lst.append((0, 0, variant_vals[0]))
                sync_history_ids = product.sync_history_ids.filtered(lambda sync_history: sync_history.is_sync == False)

                if product.ext_sync_product_id and (sync_history_ids or variant_lst):
                    sync_history_dict = {'product_id': product.id,'sync_ids': sync_history_ids.ids, 'product_variant_ids': variant_lst, 'variants_ids': variant_ids.ids}

                    for sync_history_id in sync_history_ids:
                        sync_history_dict.update({
                            sync_history_id.field_name: sync_history_id.field_value,
                        })
                    product_sync_dict.update({str(product.ext_sync_product_id):sync_history_dict})

                elif not product.ext_sync_product_id:
                    product_sync_dict.update({
                        'create' : {
                            'product_id': product.id,
                            'ext_sync_product_id': product.id,
                            'name': product.name,
                            'default_code': product.default_code,
                            'type': product.type,
                            'lst_price': product.lst_price,
                            'standard_price': product.standard_price,
                            'product_variant_ids': variant_lst,
                            'image_medium': (product.image_medium).decode("utf-8"),
                        },
                        'variants_ids': variant_ids.ids,
                    })

                if product_sync_dict:
                    product_model = self.env['odoo_external.template.binding']
                    description = "Update data from Source Databse of %s %s Database to destination Database in product.product"%(product_model,product)
                    self.env['odoo_external.template.binding'].with_delay(description=description).product_sync(product_sync_dict)
#                    product_model.with_delay(description=description).product_sync(product_sync_dict)
        
#        active model PRODUCT.PRODUCT
#        company_id = self.env.user.company_id
#        if not (company_id.db_name and company_id.host_name and company_id.user_name and company_id.password):
#            raise ValidationError("Please Configure Databse Setting")
        if active_model == 'product.product':
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
                    product_model = self.env['odoo_external.product.binding']
                    description = "Update data from Source Databse of %s %s Database to destination Database in product.product"%(product_model,product)
                    self.env['odoo_external.product.binding'].with_delay(description=description).product_sync(product_sync_dict)
#                    product_model.with_delay(description=description).product_sync(product_sync_dict)
