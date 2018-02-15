# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Online Shop Login Required',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Website',
    'license': "AGPL-3",
    'description': """
This module retricts the access of guest user to the following pages:
1. Shop page
2. Product page
3. Shopping Cart page
    """,
    'summary': "",
    'depends': [
        'website_sale',
        'website_sale_options',
    ],
    'data': [
    ],
    'installable': True,
}
