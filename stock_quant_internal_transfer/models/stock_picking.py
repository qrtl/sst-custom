# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    quant_ids = fields.One2many(
        'stock.quant',
        'picking_id',
        string="Quants",
        readonly=True,
    )
    quant_count = fields.Integer(
        compute="_compute_quant_count",
        store=True,
        string="Quants #"
    )

    @api.depends('quant_ids')
    def _compute_quant_count(self):
        for picking in self:
            picking.quant_count = len(picking.quant_ids.ids)

    @api.multi
    def action_open_quants(self):
        self.ensure_one()
        action = self.env.ref("stock.lot_open_quants")
        action_res = action.read([])[0]
        action_res['domain'] = [('picking_id', '=', self.id)]
        action_res['context'] = {}
        return action_res
