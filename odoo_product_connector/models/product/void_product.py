# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# import odoolib
import odoorpc

from odoo import models, fields, api
from odoo.addons.queue_job.job import job

FIELD_TYPE = [
        'integer',
        'float',
        'char',
        'date',
        'datetime',
        'text',
        'boolean',
        'binary',
    ]

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ext_sync_product_id = fields.Integer(
        string="External Sync Product ID",
    )
    sync_history_ids = fields.One2many(
        'product.sync.history',
        'product_tmpl_id',
        string='Sync Histories'
    )

    @api.model
    @job
    def product_sync(self, data=None):
        company_id = self.env.user.company_id
        USER = company_id.user_name
        PASSWORD = company_id.password
        HOSTNAME = company_id.host_name
        DATABASE = company_id.db_name
        PORT = company_id.port

        for product_data in data:
            # connection = odoolib.get_connection(hostname=HOSTNAME, database=DATABASE, \
            #             login=USER, password=PASSWORD)
            odoo = odoorpc.ODOO(HOSTNAME, port=PORT)
            odoo.login(DATABASE, USER, PASSWORD)
            if product_data != 'variants_ids':
                product_id = self.browse(int(data[product_data].get('product_id')))

                # product_model = connection.get_model("product.product")
                product_model = odoo.env['product.template']
                sync_result = product_model.update_data_sync(data)
                for result in sync_result:
                    product_id.update({'ext_sync_product_id': result})
                    if sync_result[result].get('sync_ids'):
                        sync_history_ids = self.env['product.sync.history'].browse(sync_result[result].get('sync_ids'))
                        sync_history_ids.write({'is_sync': True})
                    for product_varinat_id in sync_result[result].get('product_variant_ids'):
                        variant_id = self.env['product.product'].browse(int(product_varinat_id))
                        variant_id.update({'ext_sync_product_id':sync_result[result].get('product_variant_ids')[product_varinat_id]})
        return []

    @api.multi
    def write(self, vals):
        sync_history_lst = []
        for rec in self:
            if not rec.ext_sync_product_id:
                return super(ProductTemplate, self).write(vals)

        for product_vals in vals:
            for name, field in self._fields.items():
                if name == product_vals and field.type in FIELD_TYPE and name != 'ext_sync_product_id':
                    sync_history_lst.append((0, 0, {
                        'field_name':name,
                        'field_value':vals[name],
                    }))
        vals.update({'sync_history_ids': sync_history_lst})

        return super(ProductTemplate, self).write(vals)

class Product(models.Model):
    _inherit = 'product.product'

    ext_sync_product_id = fields.Integer(
        string="External Sync Product ID",
    )
    sync_history_ids = fields.One2many(
        'product.sync.history',
        'product_id',
        string='Sync Histories'
    )

    @api.model
    @job
    def product_sync(self, data=None):
        company_id = self.env.user.company_id
        USER = company_id.user_name
        PASSWORD = company_id.password
        HOSTNAME = company_id.host_name
        DATABASE = company_id.db_name
        PORT = company_id.port

        for product_data in data:
            # connection = odoolib.get_connection(hostname=HOSTNAME, database=DATABASE, \
            #             login=USER, password=PASSWORD)
            odoo = odoorpc.ODOO(HOSTNAME, port=PORT)
            odoo.login(DATABASE, USER, PASSWORD)
            product_id = self.browse(int(data[product_data].get('product_id')))

            # product_model = connection.get_model("product.product")
            product_model = odoo.env['product.product']
            sync_result = product_model.update_data_sync(data)

            for result in sync_result:
                product_id.update({'ext_sync_product_id': result})
                product_id.product_tmpl_id.write({'ext_sync_product_id': product_model.browse(int(result)).product_tmpl_id.id})
                if sync_result[result].get('sync_ids'):
                    sync_history_ids = self.env['product.sync.history'].browse(sync_result[result].get('sync_ids'))
                    sync_history_ids.write({'is_sync': True})
        return []

    @api.multi
    def write(self, vals):
        sync_history_lst = []
        for rec in self:
            if not rec.ext_sync_product_id:
                return super(Product, self).write(vals)

        for product_vals in vals:
            for name, field in self._fields.items():
                if name == product_vals and field.type in FIELD_TYPE and name != 'ext_sync_product_id':
                    sync_history_lst.append((0, 0, {
                        'field_name':name,
                        'field_value':vals[name],
                    }))
        vals.update({'sync_history_ids': sync_history_lst})

        return super(Product, self).write(vals)


class ProductSyncHistory(models.Model):
    _name = 'product.sync.history'

    field_name = fields.Char(
        string="Field",
        required=True,
    )
    field_value = fields.Char(
        string="Field Value",
        required=True,
    )
    is_sync = fields.Boolean(
        string="Is Sync",
    )
    sync_date = fields.Datetime(
        string="Sync Date",
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product Variant',
    )
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product',
    )
