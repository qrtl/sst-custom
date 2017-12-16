# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Quant Internal Transfer',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Warehouse',
    'license': 'AGPL-3',
    'summary': """Make internal transfer from quant""",
    'description': """
Create internal transfer for selected quant.
    """,
    'depends': [
        'stock',
    ],
    'data': [
        'wizard/quant_transfer_wizard.xml',
        'views/stock_quant.xml',
        'views/stock_picking.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
