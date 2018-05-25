# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductPublicCategory(models.Model):
    _name = "product.public.category"
    _inherit = [
        'product.public.category',
        'mail.thread',
        'mail.activity.mixin',
        'portal.mixin'
    ]

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
        category_ids = [i['id'] for i in result]
        category_ids.append(self.id)
        category_ids = self.browse(category_ids)
        return category_ids

    @api.multi
    def _add_category_follower(self, partner):
        subscribe_categories = self.browse()
        if partner:
            for category in self:
                category_ids = category._get_child_category()
                category_ids.message_subscribe(partner_ids=partner.ids)
                subscribe_categories += category_ids
        return subscribe_categories

    @api.multi
    def _remove_category_follower(self, partner):
        unsubscribe_categories = self.browse()
        if partner:
            for category in self:
                category_ids = category._get_child_category()
                category_ids.message_unsubscribe(partner_ids=partner.ids)
                unsubscribe_categories += category_ids
        return unsubscribe_categories
