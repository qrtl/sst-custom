# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoorpc

from odoo import models, fields, api
from odoo.addons.queue_job.job import job


class odoo_external_backend(models.Model):
    _name = 'odoo_external.backend'
    _inherit = 'connector.backend'
    _description = 'Product Connector Backend Configuration'
    _backend_type = 'odoo'

    name = fields.Char(
        string='name'
    )
    db_name = fields.Char(
        "Database Name",
    )
    port = fields.Char(
        "Port",
    )
    password = fields.Char(
        'Password',
        size=40
    )
    user_name = fields.Char(
        'User Name',
    )
    host_name = fields.Char(
        'Host Name',
    )


class ConnectorTemplateBinding(models.Model):
    _name = 'odoo_external.template.binding'
    _inherit = 'external.binding'
    _inherits = {'product.template': 'odoo_id'}

    backend_id = fields.Many2one(
        comodel_name='odoo_external.backend',
        string='Backend',
        required=True,
        ondelete='restrict',
    )
    external_id = fields.Integer(string='ID on External')
    odoo_id = fields.Many2one(comodel_name='product.template',
                              string='Product Template',
                              required=True,
                              index=True,
                              ondelete='restrict')

    _sql_constraints = [
        ('odoo_external_binding_uniq', 'unique(backend_id, external_id)',
         "A binding already exists for this record"),
    ]

    @job
    @api.multi
    def product_sync(self, data=None):
        backend_id = self.env['odoo_external.backend'].search([],limit=1)
        USER = backend_id.user_name
        PASSWORD = backend_id.password
        HOSTNAME = backend_id.host_name
        DATABASE = backend_id.db_name
        PORT = backend_id.port

        for product_data in data:
            odoo = odoorpc.ODOO(HOSTNAME, port=PORT)
            odoo.login(DATABASE, USER, PASSWORD)
            if product_data != 'variants_ids':
                product_id = self.env['product.template'].browse(int(data[product_data].get('product_id')))

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
        return self


class ConnectorProductBinding(models.Model):
    _name = 'odoo_external.product.binding'
    _inherit = 'external.binding'
    _inherits = {'product.product': 'odoo_id'}

    backend_id = fields.Many2one(
        comodel_name='odoo_external.backend',
        string='Backend',
        required=True,
        ondelete='restrict',
    )
    external_id = fields.Integer(
        string='ID on External'
    )
    odoo_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
        index=True,
        ondelete='restrict'
    )

    _sql_constraints = [
        ('odoo_external_binding_uniq', 'unique(backend_id, external_id)',
         "A binding already exists for this record"),
    ]

    @job
    @api.multi
    def product_sync(self, data=None):
        backend_id = self.env['odoo_external.backend'].search([],limit=1)
        USER = backend_id.user_name
        PASSWORD = backend_id.password
        HOSTNAME = backend_id.host_name
        DATABASE = backend_id.db_name
        PORT = backend_id.port

        for product_data in data:
            odoo = odoorpc.ODOO(HOSTNAME, port=PORT)
            odoo.login(DATABASE, USER, PASSWORD)
            product_id = self.env['product.product'].browse(int(data[product_data].get('product_id')))

            product_model = odoo.env['product.product']
            sync_result = product_model.update_data_sync(data)

            for result in sync_result:
                product_id.update({'ext_sync_product_id': result})
                product_id.product_tmpl_id.write({'ext_sync_product_id': product_model.browse(int(result)).product_tmpl_id.id})
                if sync_result[result].get('sync_ids'):
                    sync_history_ids = self.env['product.sync.history'].browse(sync_result[result].get('sync_ids'))
                    sync_history_ids.write({'is_sync': True})
        return []

#from odoo.addons.component.core import AbstractComponent

#class Exporter(AbstractComponent):
#    """ Synchronizer for exporting data from Odoo to a backend """

#    _name = 'odoo_external.exporter'
#    _inherit = 'base.synchronizer'
#    _usage = 'exporter'
#    _base_mapper_usage = 'export.mapper'

