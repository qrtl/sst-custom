# -*- coding: utf-8 -*-

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _process_product_archive(self):
        product_obj = self.env['product.product']

        self.env.cr.execute("""
            SELECT
                SUM(pol.product_qty) as product_qty,
                pr.id as product_id
            FROM
                purchase_order po
            LEFT JOIN purchase_order_line pol
                ON (pol.order_id = po.id)
            LEFT JOIN product_product pr
                ON (pol.product_id = pr.id)
            LEFT JOIN product_template pt
                ON (pr.product_tmpl_id = pt.id)
            WHERE
                pt.type = 'product' AND
                po.state = 'draft' AND
                pr.active IS TRUE
            GROUP BY
                pr.id
            """)

        query_result = self.env.cr.dictfetchall()
        for result in query_result:
            product = product_obj.browse(result['product_id'])
            virtual_available = product.virtual_available
            product_qty = result['product_qty']
            if virtual_available + product_qty < 0.0:
                # if product has reordering rules then deactivate first
                if "orderpoint_ids" in product._fields:
                    if product.orderpoint_ids:
                        product.orderpoint_ids.write({'active': False})
                # deactivate product
                product.write({'active': False})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
