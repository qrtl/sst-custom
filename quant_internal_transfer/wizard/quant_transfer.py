# -*- coding: utf-8 -*-

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

        active_ids = context.get('active_ids', [])

        #  if internal transfer functionality not activated raise warning
        picking_type_id = stock_picking_type_obj.search(
            [('code', '=', 'internal')],
            limit=1
        )
        if not picking_type_id:
            raise UserError(_('Internal Transfer are not activated!'))

        quant_ids = stock_quant_obj.browse(active_ids)
        if not quant_ids:
            raise UserError(_('Please select quant!'))

        source_location = quant_ids[0].location_id

        #  if selected quants are from different location then raise to
        #  avoid confusion of taking source location for picking
        if any(q.location_id != source_location for q in quant_ids):
            raise UserError(_('Please select valid quants!'))

        #  if any quant is already transferred from selected quant then raise
        if any(q.picking_id for q in quant_ids):
            raise Warning(_('Some quants are already transfered!'))

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
        quant_ids.write({'picking_id': picking_id.id})

        action = self.env.ref('stock.action_picking_tree_all')
        action_vals = action.read()[0]
        action_vals['domain'] = str([('id', '=', picking_id.id)])
        return action_vals

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
