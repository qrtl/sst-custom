# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for inventory functions',
    'version': '11.0.1.0.1',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'stock',
        'delivery',
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
}
