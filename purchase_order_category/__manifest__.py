# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Purchase Order Category",
    "version": "11.0.1.0.1",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Purchase",
    "license": "LGPL-3",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "data/purchase_category_data.xml",
        "views/purchase_order_views.xml",
        "views/purchase_category_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
