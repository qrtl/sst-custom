# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product Archive Cron',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Extra Tools',
    'license': "AGPL-3",
    'description': """
A cron task that will "Archive" products which have met certain conditions.
    - Target products to "Archive": The product has to be a Stockable product
    and (virtual_available + quantity requested in draft purchase.order) < 0
    """,
    'summary': """Make product archive if product virtual quantity
    +  purchase quantity is less the zero""",
    'depends': [
        'purchase'
    ],
    'data': [
        'data/cron_data.xml',
    ],
    'installable': True,
}
