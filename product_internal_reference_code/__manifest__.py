# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Internal Reference Code",
    "version": "11.0.1.1.0",
    "category": "Sales",
    "author": "Quartile Limited",
    "website": "https://www.odoo-asia.com",
    "depends": ["product"],
    "license": "AGPL-3",
    "summary": """
        Product is created, system will auto-generate a sequential number for
        default_code.
    """,
    "post_init_hook": "_create_ir_sequence",
    "application": False,
    "installable": True,
}
