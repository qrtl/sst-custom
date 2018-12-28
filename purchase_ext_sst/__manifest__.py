# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for purchase functions',
    'version': '11.0.1.12.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Purchase',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'hr',
        'purchase',
        'purchase_order_user',
        'po_so_field',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/request_channel_data.xml',
        'data/purchase_category_data.xml',
        'views/request_channel_views.xml',
        'views/request_medium_views.xml',
        'views/purchase_category_views.xml',
        'views/purchase_order_views.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
}
