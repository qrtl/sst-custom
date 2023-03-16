# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Japan Address Layout',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Extra Tools',
    'license': "AGPL-3",
    'description': """
This module provides the Japan address input field layout.
    """,
    'summary': "",
    'depends': [
        'base',
    ],
    'data': [
        'views/res_partner_views.xml',
        'data/res_country_data.xml',
    ],
    'installable': True,
}
