# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Products\' Yahoo Auction information',
    'version': '11.0.1.0.3',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Product',
    'license': "AGPL-3",
    'description': "Added fields to hold information from Yahoo Auctions to "
                   "product",
    'depends': [
        'product',
        'delivery',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/delivery_carrier_data.xml',
        'data/delivery_carrier_size_data.xml',
        'data/yahoo_product_state.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
}
