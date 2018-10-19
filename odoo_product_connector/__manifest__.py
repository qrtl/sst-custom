# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Odoo Product Connector',
    'version': '11.0.1.0.0',
    'category' : 'Connector',
    'license': 'AGPL-3',
    'summary': """This module allow to send product updates to the other Database.""",
    'description': """
    - This module allow to send product updates to the another Databse

    - Need to be configured Databse setting
        - Addded Configuration Setting to the Company Form
        - Access this setting when run the Job

    - This module allow to send product updates
        - On the Product form add Sync History to know which fields need to be update
        - Update Products from the wizard to sync
        - It's create job at the sync time
        - Job will be run when other job has been stoped

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
        # 'wizard/product_sync_view.xml',
        # 'views/backend_view.xml',
        # 'views/product_view.xml',
        'views/odoo_backend_views.xml',
        'views/connector_odoo_menu.xml',
        'data/connector_odoo_data.xml',
    ],
    'installable': True,
}
