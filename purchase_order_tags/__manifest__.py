# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Purchase Order Tags",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "category": "Purchase Management",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_tag_views.xml",
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
