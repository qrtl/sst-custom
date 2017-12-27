# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QuantTransferWizard(models.TransientModel):
    _name = 'quant.transfer.wizard'

    destination_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        required=True,
    )

    @api.multi
    def action_stock_quant_transfer(self):
        context = dict(self._context or {})
        stock_quant_obj = self.env['stock.quant']
        stock_move_obj = self.env['stock.move']
        stock_picking_obj = self.env['stock.picking']
        stock_picking_type_obj = self.env['stock.picking.type']
        stock_warehouse_obj = self.env['stock.warehouse']

        active_ids = context.get('active_ids', [])

        quant_ids = stock_quant_obj.browse(active_ids)
        if not quant_ids:
            raise UserError(_('Please select quant(s) for the internal '
                              'transfer.'))

        source_location = quant_ids[0].location_id

        #  if selected quants are from different location then raise to
        #  avoid confusion of taking source location for picking
        if any(q.location_id != source_location for q in quant_ids):
            raise UserError(_('Please select quants that are in the same '
                              'Location.'))

        stock_move_list = stock_move_obj.search([
            ('state', 'not in', ['done', 'cancel']),
            ('product_id', 'in', quant_ids.product_id.ids)
        ])
        #  if any quant is already transferred from selected quant then raise
        if stock_move_list:
            raise UserError(_('Some of the selected quants are being '
                              'transferred internally.'))

        location_list = []
        location = source_location
        while location:
            location_list.append(location.id)
            location = location.location_id

        warehouse_id = stock_warehouse_obj.search(
            [('view_location_id', 'in', location_list)],
            limit=1
        )
        if not warehouse_id:
            raise UserError(_('The stock location does not belong to any '
                              'warehouse.'))

        picking_type_domain = [('code', '=', 'internal')]
        picking_type_domain.append(('warehouse_id', '=', warehouse_id.id))

        #  if internal transfer functionality not activated raise warning
        picking_type_id = stock_picking_type_obj.search(
            picking_type_domain,
            limit=1
        )
        if not picking_type_id:
            raise UserError(_('Please check if there is internal operation '
                              'type for the warehouse'))

        origin_name = ','.join([q.display_name for q in quant_ids])

        #  prepare values for picking
        picking_vals = {
            'location_id': source_location.id,
            'picking_type_id': picking_type_id.id,
            'location_dest_id': self.destination_location_id.id,
            'origin': origin_name,
        }

        #  prepare moves
        picking_lines = []
        for quant in quant_ids:
            line_vals = {
                'product_id': quant.product_id.id,
                'product_uom_qty': quant.quantity,
            }
            new_move = stock_move_obj.new(line_vals)
            new_move.onchange_product_id()
            move_dict = stock_move_obj._convert_to_write({
                name: new_move[name] for name in new_move._cache
            })
            picking_lines.append((0, 0, move_dict))

        picking_vals.update({'move_lines': picking_lines})
        picking_id = stock_picking_obj.create(picking_vals)

        action = self.env.ref('stock.action_picking_tree_all')
        action_vals = action.read()[0]
        action_vals['domain'] = str([('id', '=', picking_id.id)])
        return action_vals
