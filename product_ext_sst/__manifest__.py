# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Extension for product",
    "version": "11.0.3.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Product",
    "license": "AGPL-3",
    "depends": [
        "website_sale",
        "purchase_order_category",  # purchase_category_id
        "product_yahoo_auction_sst",
        "product_delivery_destination",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_price_record_views.xml",
        "views/product_state_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
