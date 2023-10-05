# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xmlrpc.client

from odoo import SUPERUSER_ID, api, models


class PartnerDataMigration(models.Model):
    _name = "partner.data.migration"

    def _run_partner_data_migration(self):
        instance = self.env["odoo.instance"].search([])
        # Authenticate for v11
        common_v11 = xmlrpc.client.ServerProxy(
            "{}/xmlrpc/2/common".format(instance.instance_url)
        )
        uid_v11 = common_v11.authenticate(
            instance.instance_db, instance.login, instance.password, {}
        )
        # Fetch partners from v11
        models_v11 = xmlrpc.client.ServerProxy(
            "{}/xmlrpc/2/object".format(instance.instance_url)
        )
        domain = [("user_ids", "=", False)]
        partners_v11 = models_v11.execute_kw(
            instance.instance_db,
            uid_v11,
            instance.password,
            "res.partner",
            "search_read",
            [domain],
        )
        # Insert partners into v15 with all fields and their original IDs
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
        for partner in partners_v11:
            if partner.pop("customer", False):
                partner["customer_rank"] = 1
            if partner.pop("supplier", False):
                partner["supplier_rank"] = 1
            fields_to_remove = [
                "image",
                "image_medium",
                "image_small",
                "message_last_post",
                "opt_out",
                "website_message_ids",
                "debit_limit",
                "ref_company_ids",
                "last_time_entries_checked",
                "website_meta_title",
                "website_meta_description",
                "website_meta_keywords",
                "website_description",
                "website_short_description",
                "contracts_count",
            ]
            for field in fields_to_remove:
                partner.pop(field, None)
            for field, value in list(
                partner.items()
            ):  # We use list() to copy items as we're modifying the dictionary during iteration
                if isinstance(value, tuple) or isinstance(value, list):
                    partner.pop(field, None)
            # Directly create the partner in the current v15 database using the fetched data
            env["res.partner"].create(partner)
