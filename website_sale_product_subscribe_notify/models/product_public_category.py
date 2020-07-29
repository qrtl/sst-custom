# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _name = "product.public.category"
    _inherit = [
        "product.public.category",
        "mail.thread",
        "mail.activity.mixin",
        "portal.mixin",
    ]

    subscribe_point = fields.Integer(
        string="Subscription Points", required=True, default=1,
    )
    total_subscribe_points = fields.Integer(compute="_compute_total_subscribe_points",)

    @api.model
    def _get_child_category(self):
        query = """
            WITH RECURSIVE children AS (
                SELECT
                    id,
                    1 AS depth
                FROM
                    product_public_category
                WHERE
                    parent_id=%s
                UNION ALL
                    SELECT
                        a.id,
                        depth+1
                    FROM
                        product_public_category a
                JOIN
                    children b ON(a.parent_id = b.id)
            )
            SELECT * FROM children
        """
        self._cr.execute(query % self.id)
        result = self._cr.dictfetchall()
        category_ids = [i["id"] for i in result]
        category_ids.append(self.id)
        category_ids = self.browse(category_ids)
        return category_ids

    @api.multi
    def _compute_total_subscribe_points(self):
        for category in self:
            category.total_subscribe_points = 0
            if category.child_id:
                child_category_list = category._get_child_category()
                for child_category in child_category_list:
                    if not child_category.child_id:
                        category.total_subscribe_points += (
                            child_category.subscribe_point
                        )
