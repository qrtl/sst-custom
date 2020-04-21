# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Sales Wishlist Archive Cron",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Website",
    "license": "AGPL-3",
    "description": """
    A cron task that will "Archive" all the wishlist items that the product is
    inactive
        """,
    "depends": ["website_sale_wishlist"],
    "data": ["data/cron_data.xml"],
    "installable": True,
}
