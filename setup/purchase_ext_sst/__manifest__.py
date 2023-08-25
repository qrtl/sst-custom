# Copyright 2017-2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Extension for purchase functions",
    "version": "11.0.1.13.1",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Purchase",
    "license": "LGPL-3",
    "depends": ["hr", "purchase_convert_sale"],
    "data": [
        "security/ir.model.access.csv",
        "data/purchase_category_data.xml",
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
