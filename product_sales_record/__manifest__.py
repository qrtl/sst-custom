# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product Sales Record',
    'version': '11.0.1.0.2',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Product',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'account',
        'product',
        'sale',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
}
