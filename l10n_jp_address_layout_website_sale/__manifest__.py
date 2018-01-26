# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Japan Address Layout in E-commerce and website',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Extra Tools',
    'license': "AGPL-3",
    'description': """
This module provides the Japan address input field layout in E-commerce.
The following default address input form are change:

1. 「My Account」→ 「Change Details」 
2. During the checkout process, 「Shipping & Billing」

The module also adds a new website configuration (General Settings →
Website) to define a default country value for the website form.

If you have any inquiries, please free feel to contact us via info@quartile.co 
    """,
    'summary': "",
    'depends': [
        'portal',
        'website_sale',
    ],
    'data': [
        'views/templates.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
}
