# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import SUPERUSER_ID, api, models


class ProductCategoryDataMigration(models.Model):
    _name = "product.category.data.migration"
    _inherit = "data.migration"

    def _run_product_category_data_migration(self):
        instance, uid_v11, models_v11 = self._data_migration_authentication()
        category_v11 = models_v11.execute_kw(
            instance.instance_db,
            uid_v11,
            instance.password,
            "product.category",
            "search_read",
            [],
        )
        top_level_category = [
            category for category in category_v11 if not category.get("parent_id")
        ]
        child_category = [
            category for category in category_v11 if category.get("parent_id")
        ]
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
        for category in top_level_category:
            category_id = self.env["product.category"].search(
                [("name", "=", category["name"])]
            )
            if category_id:
                continue
            category_data = {
                "old_id": category["id"],
                "name": category["name"],
                # selection field doesn't store value in db
                # "property_cost_method":category["property_cost_method"],
                # "inventory_valuation": category["inventory_valuation"],
            }
            env["product.category"].create(category_data)
        for category in child_category:
            category_id = self.env["product.category"].search(
                [("name", "=", category["name"])]
            )
            if category_id:
                continue
            parent_id = self.env["product.category"].search(
                [("old_id", "=", category["parent_id"][0])]
            )
            category_data = {
                "old_id": category["id"],
                "name": category["name"],
                # "property_cost_method":category["property_cost_method"],
                # "inventory_valuation": category["inventory_valuation"],
                "parent_id": parent_id.id,
            }
            env["product.category"].create(category_data)
