# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Model\'s Custom Mail Server',
    'version': '11.0.1.0.0',
    'category': 'Others',
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'mail', 'mail_outbound_static',
    ],
    'data': ["views/ir_model_views.xml"],
}
