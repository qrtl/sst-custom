# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import SUPERUSER_ID, api, models


class UserDataMigration(models.Model):
    _name = "user.data.migration"
    _inherit = "data.migration"

    def _run_user_data_migration(self):
        instance, uid_v11, models_v11 = self._data_migration_authentication()
        users_v11 = models_v11.execute_kw(
            instance.instance_db,
            uid_v11,
            instance.password,
            "res.partner",
            "search_read",
        )
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
        for user in users_v11:
            user = self.env["res.users"].search([("login", "=", user["login"])])
            if user:
                continue
            user["old_id"] = user["id"]
            partner_id = self.env["res.partner"].search(
                [("old_id", "=", user["partner_id"][0])]
            )
            user["parent_id"] = partner_id.id
            env["res.users"].create(user)
