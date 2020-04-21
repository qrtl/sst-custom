# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Quant Internal Transfer",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.odoo-asia.com",
    "category": "Warehouse",
    "license": "AGPL-3",
    "summary": """Make internal transfer from quant""",
    "description": """
    Create internal transfer for selected stock quant(s).
        """,
    "depends": ["stock"],
    "data": ["wizard/stock_quant_transfer_wizard.xml"],
    "installable": True,
    "application": False,
}
