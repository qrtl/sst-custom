# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPickingValidateWizard(models.TransientModel):
    _name = 'stock.picking.validate.wizard'

    @api.model
    def default_get(self, fields):
        # Pass the picking types to the view
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        active_model = context.get('active_model')
        picking_ids = self.env[active_model].browse(active_ids)
        picking_type_ids = picking_ids.mapped('picking_type_id').ids
        if len(picking_type_ids) != 1:
            raise UserError(_('Please select stock operations with same '
                              'operation type.'))
        return super(StockPickingValidateWizard, self).default_get(fields)

    def action_stock_picking_validate(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        pickings = self.env['stock.picking'].browse(active_ids)
        pickings.action_assign()
        picking_to_validate = pickings.filtered(
            lambda r: r.state == 'assigned')
        wizard_vals = {'pick_ids': [(6, 0, picking_to_validate.ids)]}
        validate_wizard = self.env['stock.immediate.transfer'].create(
            wizard_vals)
        validate_wizard.process()
        res = self.env.ref('stock.action_picking_tree_all')
        res = res.read()[0]
        res['domain'] = str([('id', 'in', active_ids)])
        return res
