# Copyright 2018-2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Sales Adjustment",
    "version": "11.0.1.3.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Product",
    "license": "LGPL-3",
    "depends": [
        "mail_bcc",
        "product_state", # product_state_id
        "queue_job",
        "website_sale"
    ],
    "data": [
        "data/ir_actions.xml",
        "data/mail_template_data.xml",
        "views/res_config_settings_views.xml",
        "views/templates.xml",
        "security/website_sale_security.xml",
    ],
    "installable": True,
}
