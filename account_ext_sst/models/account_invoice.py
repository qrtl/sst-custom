# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    shop_id = fields.Many2one(
        'stock.warehouse',
        string='Shop',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if self.purchase_id:
            self.shop_id = self.purchase_id.shop_id
        return super(AccountInvoice, self).purchase_order_change()
