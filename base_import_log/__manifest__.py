# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Base Import Log',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'license': "AGPL-3",
    'description': """ 
Adds a screen to show log records for data imports.
    """,
    'summary': "",
    'data': [
        'security/import_group.xml',
        'security/ir.model.access.csv',
        'views/error_log_view.xml',
    ],
    'installable': True,
}
