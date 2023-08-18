# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Extension for product",
    "version": "11.0.3.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Product",
    "license": "LGPL-3",
    "depends": [
        "website_sale",
        "purchase_order_category",  # purchase_category_id
        "product_yahoo_auction_sst",
        "product_delivery_destination",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_state_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
