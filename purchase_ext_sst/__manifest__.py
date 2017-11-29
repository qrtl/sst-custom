# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for purchase functions',
    'version': '11.0.1.1.1',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Purchase',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'hr',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/request_channel_data.xml',
        'data/purchase_category_data.xml',
        'views/request_channel_views.xml',
        'views/request_medium_views.xml',
        'views/purchase_category_views.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
}
