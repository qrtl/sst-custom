# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    shop_ids = fields.Many2many(
        'stock.warehouse',
        string='Shop',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @api.onchange('invoice_line_ids')
    def invoice_line_ids_onchange(self):
        shop_ids = []
        if self.invoice_line_ids:
            for invoice_line_id in self.invoice_line_ids:
                if invoice_line_id.purchase_id and \
                        invoice_line_id.purchase_id.shop_id and \
                        invoice_line_id.purchase_id.shop_id.id not in shop_ids:
                    shop_ids.append(invoice_line_id.purchase_id.shop_id.id)
            self.shop_ids = shop_ids

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        res.invoice_line_ids_onchange()
        return res
