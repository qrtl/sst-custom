# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import SUPERUSER_ID, api, models


class PartnerDataMigration(models.Model):
    _name = "partner.data.migration"
    _inherit = "data.migration"
    _description = "Partner Data Migration"

    def _run_partner_data_migration(self):
        instance, uid_v11, models_v11 = self._data_migration_authentication()
        partners_v11 = models_v11.execute_kw(
            instance.instance_db,
            uid_v11,
            instance.password,
            "res.partner",
            "search_read",
            [],
            {"limit": 100},
        )
        top_level_partners = [
            partner for partner in partners_v11 if not partner.get("parent_id")
        ]
        child_partners = [
            partner for partner in partners_v11 if partner.get("parent_id")
        ]
        # Insert partners into v15 with all fields and their original IDs
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
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
            "commercial_partner_country_id",
            "calendar_last_notif_ack",
            "is_invoice_issuer",
            "member_group_id",
            "seller",
            "state",
            "set_seller_wise_settings",
            "gender",
            "identification_number",
            "date_of_birth",
            "remaining_point_limit",
            "commission",
            "auto_product_approve",
            "seller_payment_limit",
            "next_payment_request",
            "total_mp_payment",
            "paid_mp_payment",
            "balance_mp_payment",
            "available_amount",
            "profile_image",
            "cart_update_message",
            "task_count",
            "cashable_amount",
            "sol_count",
            "allow_product_variants",
        ]
        for partner in top_level_partners:
            if partner.pop("customer", False):
                partner["customer_rank"] = 1
            if partner.pop("supplier", False):
                partner["supplier_rank"] = 1
            for field in fields_to_remove:
                partner.pop(field, None)
            for field, value in list(partner.items()):
                # We use list() to copy items as we're modifying the dictionary during iteration
                if isinstance(value, tuple) or isinstance(value, list):
                    partner.pop(field, None)
            # Directly create the partner in the current v15 database using the fetched data
            partner["old_id"] = partner["id"]
            env["res.partner"].create(partner)

        for partner in child_partners:
            if partner.pop("customer", False):
                partner["customer_rank"] = 1
            if partner.pop("supplier", False):
                partner["supplier_rank"] = 1
            for field in fields_to_remove:
                partner.pop(field, None)
            for field, value in list(partner.items()):
                # We use list() to copy items as we're modifying the dictionary during iteration
                if field != "parent_id" and (
                    isinstance(value, tuple) or isinstance(value, list)
                ):
                    partner.pop(field, None)
            if partner.get("parent_id"):
                parent_id = self.env["res.partner"].search(
                    [("old_id", "=", partner["parent_id"][0])]
                )
                partner["parent_id"] = parent_id.id
            # Directly create the partner in the current v15 database using the fetched data
            partner["old_id"] = partner["id"]
            env["res.partner"].create(partner)
