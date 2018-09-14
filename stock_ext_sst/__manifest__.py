# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extension for inventory functions',
    'version': '11.0.2.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'sale',
        'stock',
        'delivery',
        'product_yahoo_auction_sst',
        'stock_quant_list_view',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
        'wizard/stock_quant_status_update_wizard.xml',
    ],
    'installable': True,
}
