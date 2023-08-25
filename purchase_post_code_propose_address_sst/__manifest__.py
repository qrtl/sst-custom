# Copyright 2019-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Post Code (JP) Propose Purchase Order Address",
    "version": "11.0.1.0.1",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Purchase",
    "license": "AGPL-3",
    "depends": ["purchase"],
    "external_dependencies": {"python": ["jaconv"]},
    "data": ["views/purchase_order_views.xml"],
    "installable": True,
}
