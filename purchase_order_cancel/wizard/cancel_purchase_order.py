# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from odoo import models, api, _


class CancelPurchaseOrder(models.TransientModel):
    _name = 'cancel.purchase.order'

    @api.model
    def _cancel_purchase_order(self, orders):
        return orders.button_cancel()

    @api.multi
    def action_cancel_purchase_order(self):
        active_ids = self._context.get('active_ids', [])
        active_model = self._context.get('active_model', 'purchase.order')
        orders = self.env[active_model].browse(active_ids)

        if any([order.state != 'draft' for order in orders]):
            raise Warning(_('Error!, You can not cancel non-draft orders!'))

        self._cancel_purchase_order(orders)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
