# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quant_ids = fields.One2many(
        'stock.quant',
        'sale_order_id',
        string="Quants",
    )
    quant_count = fields.Integer(
        compute="_compute_quant_count",
        store=True,
        string="Quants #"
    )

    @api.depends('quant_ids')
    def _compute_quant_count(self):
        '''This method count a quant in sale order'''
        for order in self:
            order.quant_count = len(order.quant_ids.ids)

    @api.multi
    def action_open_quants(self):
        '''This method redirect to related sale order quant.'''
        self.ensure_one()
        action = self.env.ref("stock.lot_open_quants")
        action_res = action.read([])[0]
        action_res['domain'] = [('sale_order_id', '=', self.id)]
        action_res['context'] = {}
        return action_res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
