# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Web Sessions Management',
    'summary': 'Manage user sessions',
    'author': 'TKO',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'website': 'http://tko.tko-br.com',
    'depends': [
        'resource',
    ],
    'external_dependencies': {
        'python': ['num2words'],
    },
    'images': ['static/description/sessions_groups.png',
               'static/description/sessions_management.png',
               'static/description/sessions_pivot.png',
               'static/description/sessions_user_preferences.png',
               'static/description/sessions_users.png',],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/res_users_view.xml',
        'views/res_groups_view.xml',
        'views/ir_sessions_view.xml',
        'views/webclient_templates.xml',
    ],
    'application': False,
}
