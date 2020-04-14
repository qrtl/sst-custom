# -*- coding: utf-8 -*-
# Copyright 2018-2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Odoo Product Subscribe Notify',
    'version': '11.0.2.0.1',
    'category': 'Website',
    'license': 'LGPL-3',
    'summary': "Send notification to subscribers",
    'description': """
This module allows to send notification to the subscribers of the category if
any following fields of the product is updated,
- website_published
- vid_path
- list_price
    """,
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'depends': [
        'mail_adj_sst',
        'mail_bcc',
        'website_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/templates.xml',
        'views/member_group_views.xml',
        'views/product_public_category_view.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': False,
}
