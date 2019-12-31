# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Email BCC',
    'summary': 'Add BCC field to message and template',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited'
              'Odoo Community Association (OCA)',
    'website': 'http://github.com/OCA/social',
    'category': 'Social Network',
    'license': "AGPL-3",
    'depends': [
        'mail',
    ],
    'data': [
        'views/mail_mail_views.xml',
        'views/mail_template_views.xml',
    ],
    'installable': True,
}
