# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Forum Adjustment",
    "version": "11.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Website",
    "license": "AGPL-3",
    "depends": ["website_forum"],
    "data": [
        "data/mail_data.xml",
        "views/ir_mail_server_views.xml",
        "views/res_config_settings_views.xml",
        "views/website_forum.xml",
    ],
    "qweb": ["static/src/xml/website_forum_share_templates.xml"],
    "installable": True,
}
