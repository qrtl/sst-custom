# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Virtual Available Adjust',
    'version': '11.0.1.2.1',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Warehouse',
    'license': 'AGPL-3',
    'summary': """""",
    'description': """
Deduct quantities of unconfirmed sales orders from forcasted quantity
calculation.
    """,
    'depends': [
        'stock',
        'website_sale',
        'product_ext_sst',
    ],
    'data': [
        'views/product_views.xml',
    ],
    'installable': True,
}
