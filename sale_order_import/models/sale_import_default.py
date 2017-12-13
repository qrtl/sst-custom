# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleImportDefault(models.Model):
    _name = 'sale.import.default'

    company_id = fields.Many2one(
        'res.company',
        required=True,
        string='Company',
    )
    picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        required=True,
        string='Shipping Policy',
    )
    customer_invoice_journal_id = fields.Many2one(
        'account.journal',
        required=True,
        string='Customer Invoice Journal',
    )
    customer_payment_journal_id = fields.Many2one(
        'account.journal',
        required=True,
        string='Customer Payment Journal',
    )

    _sql_constraints = [
        ('name_company_uniq', 'unique(company_id)',
         'Companies must be unique!'),
    ]

    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.customer_invoice_journal_id = False
        self.customer_payment_journal_id = False
