# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Technical features group adjustments',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Usability',
    'license': "AGPL-3",
    'description': """
This module hides the "Technical Features" option in the Preferences form view.
    """,
    'summary': "",
    'depends': [
        'base_technical_features',
    ],
    'data': [
        'views/res_users_views.xml',
    ],
    'installable': True,
}
