# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for sales functions',
    'version': '11.0.1.2.1',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Sale',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'sale_stock',
        'sale_order_dates',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
