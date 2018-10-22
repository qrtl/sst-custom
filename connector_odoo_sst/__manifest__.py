# © 2013 Guewen Baconnier,Camptocamp SA,Akretion
# © 2016 Sodexis
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Odoo Connector',
    'version': '11.0.1.0.0',
    'category' : 'Connector',
    'license': 'AGPL-3',
    'summary': """""",
    'description': """
- This module extends connector module to sync records between the master and
  satellite databases of Odoo.
- This module is based on connector_magento module (for ver. 10.0).
    """,
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'depends': [
        'product',
        'queue_job',
        'connector',
    ],
    'external_dependencies': {
        'python': ['odoorpc'],
    },
    'data':[
        'security/ir.model.access.csv',
        'views/odoo_backend_views.xml',
        'views/connector_odoo_menu.xml',
        'data/connector_odoo_data.xml',
    ],
    'installable': True,
}
