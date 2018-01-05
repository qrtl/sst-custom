# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website Sales Adjustment',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Product',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'website_sale',
        'product_ext_sst',
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
}
