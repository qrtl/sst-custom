# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Odoo Product Subscribe Notify',
    'version': '11.0.1.0.0',
    'category' : 'Website',
    'license': 'Other proprietary',
    'summary': "Send notification to subscribers",
    'description': """
This module allows to send notification to the subscribers of the category if
any following fields of the product is updated,
- website_published
- vid_path
- list_price
- description_sale
    """,
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'depends': [
        'mail_adj_sst',
        'website_sale',
    ],
    'data':[
        'data/templates.xml',
        'views/product_public_category_view.xml',
        'views/website_templates.xml',
    ],
    'installable' : True,
    'application' : False,
}
