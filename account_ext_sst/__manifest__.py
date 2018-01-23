# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for accounting functions',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Accounting',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'account',
        'purchase_ext_sst',
        'sale',
    ],
    'data': [
        'views/account_invoice_views.xml',
    ],
    'installable': True,
}
