# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Odoo Product Connector',
    'version': '1.0',
    'category' : 'Sales',
    'license': 'Other proprietary',
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
    'website': 'https://www.odoo-asia.com',
    'depends': [
        'product',
        'queue_job',
    ],
    'data':[
        'wizard/product_sync_view.xml',
        'views/product_view.xml',
        'views/res_company_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
