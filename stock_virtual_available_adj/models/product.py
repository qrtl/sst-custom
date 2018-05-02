# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.tools.float_utils import float_round


class Product(models.Model):
    _inherit = "product.product"

    draft_sale_qty = fields.Float(
        'Sale Quantity (Draft)',
        compute='_compute_quantities',
    )

    # note that below adjustment may not be desirable in case forecasted qty
    # needs to be checked at granular level (e.g. per location) as draft sales
    # order qty is deducted regardless of the applied domain
    def _compute_quantities_dict(self, lot_id, owner_id, package_id,
                                 from_date=False, to_date=False):
        res = super(Product, self)._compute_quantities_dict(
            lot_id, owner_id, package_id, from_date, to_date)
        for product in self.with_context(prefetch_fields=False):
            sale_lines = self.env['sale.order.line'].search(
                [('product_id', '=', product.id),
                 ('state', 'in', ('sent', 'draft'))])
            if sale_lines:
                sale_qty = sum(sale_lines.mapped('product_uom_qty'))
                res[product.id]['draft_sale_qty'] = sum(sale_lines.filtered(
                    lambda p: p.state == 'draft').mapped('product_uom_qty'))
                res[product.id]['virtual_available'] = float_round(
                    res[product.id]['virtual_available'] - sale_qty,
                    precision_rounding=product.uom_id.rounding)
        return res

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def _compute_quantities(self):
        res = self._compute_quantities_dict(self._context.get('lot_id'),
                                            self._context.get('owner_id'),
                                            self._context.get('package_id'),
                                            self._context.get('from_date'),
                                            self._context.get('to_date'))
        for product in self:
            product.qty_available = res[product.id]['qty_available']
            product.incoming_qty = res[product.id]['incoming_qty']
            product.outgoing_qty = res[product.id]['outgoing_qty']
            product.virtual_available = res[product.id]['virtual_available']
            if 'draft_sale_qty' in res[product.id]:
                product.draft_sale_qty = res[product.id]['draft_sale_qty']
