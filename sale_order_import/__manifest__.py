# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sales Order Import",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Sales Management",
    "license": "AGPL-3",
    "depends": [
        "delivery",
        "base_data_import",
        "queue_job",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/data_import_logs_views.xml",
        "views/res_company_views.xml",
        "views/sale_order_views.xml",
        "wizards/sale_order_import_views.xml",
    ],
    "installable": True,
}
