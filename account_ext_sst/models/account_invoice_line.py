# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    shop_id = fields.Many2one(
        related='invoice_id.shop_id',
        string='Shop',
        readonly=True,
    )

    @api.model
    def create(self, vals):
        res = super(AccountInvoiceLine, self).create(vals)
        if res.sale_line_ids:
            for order_line in res.sale_line_ids:
                if order_line.order_id.warehouse_id.id:
                    res.invoice_id.shop_id = \
                        order_line.order_id.warehouse_id.id
                    return res
