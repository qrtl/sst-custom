# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Quant Sale Order',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': """Make sale order from quant""",
    'description': """
Create sale order for selected stock quant(s).
    """,
    'depends': [
        'sale_stock',
#         'delivery',
    ],
    'data': [
             'wizard/stock_quant_sale_order_wizard.xml',
             'views/sale_order_view.xml',
             'views/stock_quant_views.xml',
    ],
    'installable': True,
    'application': False,
}
