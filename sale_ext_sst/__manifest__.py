# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for sales functions',
    'version': '11.0.1.1.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Sale',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
