# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "User Data Migration",
    "version": "15.0.1.0.0",
    "category": "Tools",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": ["data_migration"],
    "data": ["security/ir.model.access.csv", "data/user_migration_scheduler.xml"],
    "installable": True,
}
