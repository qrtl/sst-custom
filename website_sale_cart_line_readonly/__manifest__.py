# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Cart Readonly Line",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Website",
    "license": "AGPL-3",
    "description": """
    Add 'website_readonly' field to sale.order.line, when it is set to True,
    the line becomes uneditable in website.
        """,
    "depends": ["website_sale"],
    "data": ["views/templates.xml"],
    "installable": True,
}
