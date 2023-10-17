# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api, models


class PartnerDataMigration(models.Model):
    _name = "partner.data.migration"
    _inherit = ["data.migration", "data.migration.mapping"]
    _description = "Partner Data Migration"

    def _run_partner_data_migration(self):
        required_fields = [
            "is_invoice_issuer",
            "team_id",
            "identification_type_id",
            "occupation_id",
            "website_published",
            "date_of_birth",
            "company_id",
            "date",
            "title",
            "parent_id",
            # "user_id", # user migration will handle it.
            "active",
            "customer",
            "supplier",
            "employee",
            "state_id",
            "country_id",
            "is_company",
            # "commercial_partner_id", # compute function will handle it.
            "name",
            "display_name",
            "lang",
            "tz",
            "vat",
            "website",
            "comment",
            "barcode",
            "return_policy",
            "invoice_warn",
            "invoice_warn_msg",
            "picking_warn",
            "function",
            "type",
            "street",
            "street2",
            "zip",
            "city",
            "picking_warn_msg",
            "sale_warn",
            "email",
            "phone",
            "mobile",
            "sale_warn_msg",
            "shipping_policy",
            "purchase_warn",
            "purchase_warn_msg",
            "profile_msg",
            "identification_number",
            "company_name",
            "fax",
            "gender",
        ]
        instance, uid_v11, models_v11 = self._data_migration_authentication()
        partners_v11 = models_v11.execute_kw(
            instance.instance_db,
            uid_v11,
            instance.password,
            "res.partner",
            "search_read",
            [],
            {"fields": required_fields},
        )
        top_level_partners = [
            partner for partner in partners_v11 if not partner.get("parent_id")
        ]
        child_partners = [
            partner for partner in partners_v11 if partner.get("parent_id")
        ]

        for partner in top_level_partners:
            self.with_delay()._process_partner_migration(partner, is_child=False)

        for partner in child_partners:
            self.with_delay()._process_partner_migration(partner, is_child=True)

    def _process_partner_migration(self, partner, is_child=False):
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
        many2one_field_mapping = {
            "team_id": "crm.team",
            "identification_type_id": "identification.type",
            "occupation_id": "res.occupation",
            "company_id": "res.company",
            "state_id": "res.country.state",
            "country_id": "res.country",
            "title": "res.partner.title",
        }

        if partner.pop("customer", False):
            partner["customer_rank"] = 1
        if partner.pop("supplier", False):
            partner["supplier_rank"] = 1
        date_of_birth = partner.pop("date_of_birth", False)
        if date_of_birth:
            partner["date_birth"] = date_of_birth

        for field, model in many2one_field_mapping.items():
            if field in partner:
                partner[field] = self.map_many2one_field_by_name(
                    env, model, partner[field]
                )
        for field, value in list(partner.items()):
            if (not is_child or field != "parent_id") and (
                isinstance(value, tuple) or isinstance(value, list)
            ):
                partner.pop(field, None)

        if is_child and partner.get("parent_id"):
            parent_id = env["res.partner"].search(
                [("old_id", "=", partner["parent_id"][0])]
            )
            partner["parent_id"] = parent_id.id

        partner["old_id"] = partner["id"]
        env["res.partner"].create(partner)
