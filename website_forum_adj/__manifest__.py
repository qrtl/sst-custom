# Copyright 2019-2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Website Forum Adjustment',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Website',
    'license': "LGPL-3",
    'description': """
This module removes the social message part after user posts a question/answer
on website forum.
    """,
    'depends': [
        'website_forum',
        'ir_mail_server_email_from',
    ],
    'data': [
        'data/mail_data.xml',
        'views/res_config_settings_views.xml',
        'views/website_forum.xml',
    ],
    'qweb': [
        'static/src/xml/website_forum_share_templates.xml'
    ],
    'installable': True,
}
