# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product Sales Record',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Product',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'product',
        'sale',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
}
