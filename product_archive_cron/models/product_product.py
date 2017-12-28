# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _process_product_archive(self):
        product_obj = self.env['product.product']

        self.env.cr.execute("""
            WITH
                purchase_info AS(
                    SELECT
                        pol.product_qty,
                        pol.product_id
                    FROM
                        purchase_order po
                    LEFT JOIN purchase_order_line pol
                        ON (pol.order_id = po.id)
                    WHERE
                        po.state = 'draft'
                )
            SELECT
                SUM(pi.product_qty) as product_qty,
                pp.id as product_id
            FROM
                product_product pp
            LEFT JOIN product_template pt
                ON (pp.product_tmpl_id = pt.id)
            LEFT JOIN purchase_info pi
                ON (pi.product_id = pp.id)
            WHERE
                pt.type = 'product' AND
                pp.active IS TRUE
            GROUP BY
                pp.id
        """)

        query_result = self.env.cr.dictfetchall()
        for result in query_result:
            product = product_obj.browse(result['product_id'])
            virtual_available = product.virtual_available
            product_qty = result['product_qty'] or 0
            if virtual_available + product_qty < 0.0:
                # if product has reordering rules then deactivate first
                if "orderpoint_ids" in product._fields:
                    if product.orderpoint_ids:
                        product.orderpoint_ids.write({'active': False})
                # deactivate product
                product.product_tmpl_id.write({'active': False})
