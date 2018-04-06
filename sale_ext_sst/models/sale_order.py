# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    phone = fields.Char(
        related='partner_id.phone',
        string='Phone',
    )
    requested_date = fields.Datetime(
        readonly=False,
    )
    invoice_residual = fields.Monetary(
        'Invoice Amount Due',
        compute='_compute_invoice_residual',
        store=True,
        help='Remaining amount due of invoice(s).',
    )

    @api.multi
    @api.depends('invoice_ids.residual')
    def _compute_invoice_residual(self):
        for order in self:
            order.invoice_residual = order.amount_total
            for invoice in order.invoice_ids:
                if invoice.state not in ('draft', 'cancel'):
                    order.invoice_residual -= invoice.amount_total \
                                              - invoice.residual
