# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Cancel Multiple Purchase Order',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Purchases',
    'license': "AGPL-3",
    'description': """
Allow to cancel multiple purchase orders at single click!
    """,
    'summary': "Cancel Multiple Purchase Orders",
    'depends': [
        'purchase'
    ],
    'data': [
        'wizard/purchase_order_view_cancel.xml',
    ],
    'installable': True,
}
