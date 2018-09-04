# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Base View Adjustments',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Usability',
    'license': "AGPL-3",
    'description': """
This module removes the Odoo.com link from the user dropdown.
    """,
    'summary': "",
    'depends': [
        'web',
    ],
    'qweb': [
        'static/src/xml/web.xml'
    ],
    'installable': True,
}
