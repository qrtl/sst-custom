# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Category",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Purchase",
    "license": "AGPL-3",
    "depends": ["purchase_ext_sst"],
    "data": [
        "security/ir.model.access.csv",
        "data/purchase_category_data.xml",
        "views/purchase_order_views.xml",
        "views/purchase_category_views.xml",
    ],
    "installable": True,
}
