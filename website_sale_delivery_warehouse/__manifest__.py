# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Order's Delivery Warehouse",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Product",
    "license": "AGPL-3",
    "description": """
    This module adds warehouse field to the delivery method, the warehouse
    assigned to the delivery method will be set as the warehouse of the website
    order.
        """,
    "depends": ["website_sale_delivery"],
    "data": ["views/delivery_carrier_views.xml"],
    "installable": True,
}
