# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Website Sales Adjustment',
    'version': '11.0.1.2.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Product',
    'license': "LGPL-3",
    'description': """
This module modify the website_sale module and provide following feature(s):
 - Show product_state_id in the /shop/product page.
 - Hide the "Shop" menu in header from public user.
    """,
    'depends': [
        'mail_bcc',
        'product_ext_sst',
        'website_sale',
    ],
    'data': [
        'data/ir_actions.xml',
        'data/mail_template_data.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
        'security/website_sale_security.xml',
    ],
    'installable': True,
}
