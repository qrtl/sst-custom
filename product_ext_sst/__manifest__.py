# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for product',
    'version': '11.0.1.1.1',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Product',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'website_sale',
        'purchase_ext_sst',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_state_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
}
