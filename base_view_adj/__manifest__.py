# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Base View Adjustments",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Usability",
    "license": "AGPL-3",
    "summary": """
This module removes following items from the user dropdown.
    - Documentation
    - Support
    - My Odoo.com account
    """,
    "depends": ["web"],
    "qweb": ["static/src/xml/web.xml"],
    "installable": True,
}
