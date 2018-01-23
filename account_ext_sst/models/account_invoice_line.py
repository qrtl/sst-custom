# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def create(self, vals):
        res = super(AccountInvoiceLine, self).create(vals)
        if res.sale_line_ids:
            shop_ids = []
            for order_line in res.sale_line_ids:
                if order_line.order_id.warehouse_id.id and \
                                order_line.order_id.warehouse_id.id not in \
                                res.invoice_id.shop_ids.ids:
                    shop_ids.append(order_line.order_id.warehouse_id.id)
            res.invoice_id.shop_ids = shop_ids
        return res
