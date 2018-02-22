# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockPickingValidate(models.TransientModel):
    _name = 'stock.picking.validate'

    def action_stock_picking_validate(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        picking_ids = self.env['stock.picking'].browse(active_ids)
        picking_to_validate = picking_ids.filtered(lambda r: r.state == 'assigned')
        wizard_vals = {'pick_ids': [(6, 0, picking_to_validate.ids)]}
        validate_wizard = self.env['stock.immediate.transfer'].create(wizard_vals)
        validate_wizard.process()
        res = self.env.ref('stock.action_picking_tree_all')
        res = res.read()[0]
        res['domain'] = str([('id', 'in', active_ids)])
        return res
