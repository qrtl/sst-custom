# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        result = super(AccountInvoice, self).invoice_validate()
        for account_invoice in self:
            if account_invoice.state == 'open' and account_invoice.type == \
                    'out_invoice':
                for inovice_line in account_invoice.invoice_line_ids:
                    product = inovice_line.product_id.product_tmpl_id
                    product.write({
                        'sale_price_unit': inovice_line.price_subtotal /
                                           inovice_line.quantity,
                    })
        return result
