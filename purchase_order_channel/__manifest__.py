# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Channel",
    "version": "11.0.1.0.1",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Purchase",
    "license": "AGPL-3",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "data/request_channel_data.xml",
        "data/menuitem_data.xml",
        "views/purchase_order_views.xml",
        "views/request_channel_views.xml",
        "views/request_medium_views.xml",
    ],
    "installable": True,
}
