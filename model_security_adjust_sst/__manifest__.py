# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Model Security Adjust SST',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Security',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'hr',
        'stock',
    ],
    'data': [
        'security/hr_security.xml',
        'security/stock_security.xml',
        'security/ir.model.access.csv',
        'views/stock_menu_views.xml',
    ],
    'installable': True,
}
