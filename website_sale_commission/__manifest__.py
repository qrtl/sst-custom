# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Order Commission",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Website",
    "license": "AGPL-3",
    "description": """
    Internal user can assign a commission product to online cart.
        """,
    "depends": ["website_sale_cart_line_readonly"],
    "data": ["views/res_config_settings_views.xml"],
    "installable": True,
}
