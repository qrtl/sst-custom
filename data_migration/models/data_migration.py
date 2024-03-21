# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xmlrpc.client

from odoo import models


class DataMigration(models.AbstractModel):
    _name = "data.migration"
    _description = "Data Migration"

    def _data_migration_authentication(self):
        instance = self.env["odoo.instance"].search([])
        # Authenticate for v11
        common_v11 = xmlrpc.client.ServerProxy(
            "{}/xmlrpc/2/common".format(instance.instance_url)
        )
        uid_v11 = common_v11.authenticate(
            instance.instance_db, instance.login, instance.password, {}
        )
        models_v11 = xmlrpc.client.ServerProxy(
            "{}/xmlrpc/2/object".format(instance.instance_url)
        )
        return instance, uid_v11, models_v11
