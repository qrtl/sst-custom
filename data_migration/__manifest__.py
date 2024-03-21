# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Data Migration",
    "version": "15.0.1.0.0",
    "category": "Tools",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": ["base", "queue_job"],
    "data": [
        "security/ir.model.access.csv",
        "data/data_migration_scheduler.xml",
        "views/odoo_instance_views.xml",
    ],
    "installable": True,
}
