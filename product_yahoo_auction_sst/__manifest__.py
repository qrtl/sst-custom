# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Products' Yahoo Auction information",
    "version": "11.0.1.1.2",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Product",
    "license": "LGPL-3",
    "depends": ["product", "delivery"],
    "data": [
        "security/ir.model.access.csv",
        "data/delivery_carrier_data.xml",
        "data/delivery_carrier_size_data.xml",
        "data/yahoo_product_state.xml",
        "views/product_template_views.xml",
        "views/yahoo_product_state_views.xml",
    ],
    "installable": True,
}
