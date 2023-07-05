# Copyright 2017-2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Extension for purchase functions",
    "version": "11.0.1.13.1",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Purchase",
    "license": "LGPL-3",
    "depends": ["hr", "purchase", "purchase_convert_sale"],
    "data": [
        "security/ir.model.access.csv",
        "data/request_channel_data.xml",
        "data/purchase_category_data.xml",
        "views/request_channel_views.xml",
        "views/request_medium_views.xml",
        "views/purchase_category_views.xml",
        "views/purchase_order_views.xml",
        "views/hr_employee_views.xml",
    ],
    "installable": True,
}
