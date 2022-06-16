# Copyright 2017-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sales Order Import",
    "version": "11.0.1.2.0",
    "author": "Quartile Limited",
    "website": "https://www.odoo-asia.com",
    "category": "Sales Management",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "base_import_log",
        "account_voucher",
        "sale_management",
        "delivery",
        "queue_job",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/error_logs_views.xml",
        "views/sale_import_default.xml",
        "views/sale_order_views.xml",
        "wizard/import_sale_view.xml",
    ],
    "installable": True,
}
