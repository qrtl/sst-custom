# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Order Remove Product Penalty",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Website",
    "license": "AGPL-3",
    "depends": [
        "sales_team",
        "website_sale_cart_line_readonly",
        "website_sale_cart_product_check",
    ],
    "data": ["views/res_config_settings_views.xml", "views/templates.xml"],
    "installable": True,
}
