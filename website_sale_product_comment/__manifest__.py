# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Customer notification on product comment',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Website',
    'license': "AGPL-3",
    'description': """
This module will send notification to all the customers
who have already added comment for product on other comment by customer.
    """,
    'summary': "Customer notification on product comment",
    'depends': [
        'theme_stoneware',
    ],
    'data': [
        'data/templates.xml',
        'views/website_templates.xml'
    ],
    'installable': True,
}
