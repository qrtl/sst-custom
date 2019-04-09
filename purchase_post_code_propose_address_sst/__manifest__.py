# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Post Code (JP) Propose Purchase Order Address',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Purchase',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'purchase_ext_sst',
        'l10n_jp_country_state',
    ],
    'external_dependencies': {
        'python': ['jaconv'],
    },
    'data': [
        'views/purchase_order_views.xml',
    ],
    'installable': True,
}
