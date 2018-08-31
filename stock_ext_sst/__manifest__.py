# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for inventory functions',
    'version': '11.0.1.1.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'stock',
        'delivery',
        'product_yahoo_auction_sst',
        'stock_quant_list_view',
    ],
    'data': [
        'data/ir_actions.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
    ],
    'installable': True,
}
