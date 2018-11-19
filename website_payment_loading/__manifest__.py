# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website Payment Loading Screen',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Payment',
    'license': "AGPL-3",
    'description': """
This module modify the payment page, add a loading screen after user presses
the "Pay Now" button.
    """,
    'depends': [
        'payment',
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
}
