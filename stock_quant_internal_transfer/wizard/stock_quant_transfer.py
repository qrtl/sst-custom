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

        active_ids = context.get('active_ids', [])
        quant_ids = stock_quant_obj.browse(active_ids)
        source_location = quant_ids[0].location_id

        #  if selected quants are from different location then raise to
        #  avoid confusion of taking source location for picking
        if any(q.location_id != source_location for q in quant_ids):
            raise UserError(_('Please select quants that are in the same '
                              'Location.'))

        # Check if any quants are already in any internal stock move,
        self.check_exist_stock_moves(quant_ids, source_location)

        # Get the picking type
        picking_type = self.get_picking_type(source_location)

        origin_name = ','.join([q.display_name for q in quant_ids])

        #  prepare values for picking
        picking_vals = {
            'location_id': source_location.id,
            'picking_type_id': picking_type.id,
            'location_dest_id': self.destination_location_id.id,
            'origin': origin_name,
        }

        #  prepare moves
        picking_lines = []
        for quant in quant_ids:
            line_vals = {
                'product_id': quant.product_id.id,
                'product_uom_qty': quant.quantity,
                'picking_type_id': picking_type.id,
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

    def check_exist_stock_moves(self, quant_ids, location_id):
        stock_move_obj = self.env['stock.move']
        stock_picking_type_obj = self.env['stock.picking.type']

        internal_stock_picking_types = stock_picking_type_obj.search([
            ('code', '=', 'internal')
        ])
        stock_move_list = stock_move_obj.search([
            ('state', 'not in', ['done', 'cancel']),
            ('location_id', '=', location_id.id),
            ('picking_type_id', 'in', internal_stock_picking_types.ids),
            ('product_id', 'in', [q.product_id.id for q in quant_ids])
        ])
        if stock_move_list:
            error_msg = ''
            for stock_move in stock_move_list:
                error_msg += '\n%s: %s' % (
                    stock_move.reference,
                    stock_move.product_id.display_name,
                )
            raise UserError(_('Some of the selected quants are being '
                              'processed by other internal Stock Move. '
                              'Please process the following Stock Moves '
                              'before creating new internal moves:%s' %
                              error_msg))

    def get_picking_type(self, location_id):
        stock_picking_type_obj = self.env['stock.picking.type']
        stock_warehouse_obj = self.env['stock.warehouse']

        location_list = []
        location = location_id
        while location:
            location_list.append(location.id)
            location = location.location_id

        source_warehouse_id = stock_warehouse_obj.search(
            [('view_location_id', 'in', location_list)],
            limit=1
        )
        if not source_warehouse_id:
            raise UserError(_('The stock location does not belong to any '
                              'warehouse.'))

        # if internal transfer functionality not activated raise warning
        picking_type_id = stock_picking_type_obj.search(
            [('code', '=', 'internal'),
             ('warehouse_id', '=', source_warehouse_id.id)],
            limit=1
        )
        if not picking_type_id:
            raise UserError(_('Please check if there is internal operation '
                              'type for the warehouse'))
        return picking_type_id
