# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Extension for partner",
    "version": "11.0.1.1.0",
    "author": "Quartile Limited",
    "website": "https://www.odoo-asia.com",
    "category": "Purchase",
    "license": "AGPL-3",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_identification_type_views.xml",
        "views/res_occupation_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
