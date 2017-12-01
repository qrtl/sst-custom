# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    internal_code_prefix = fields.Char(
        string="Internal Reference Prefix",
        copy=False,
        require=True,
        help="A prefix code which is used to automatically generate the "
             "internal reference when creating a new product."
    )

    @api.multi
    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        # Create the sequence for the company upon creation
        if 'internal_code_prefix' in vals:
            prefix = vals['internal_code_prefix']
        seq = {
            'name': res.name + ' - Product Sequence',
            'code': 'product.product.internal_code',
            'prefix': prefix or '',
            'padding': 5,
            'number_increment': 1,
            'company_id': res.id,
        }
        self.env['ir.sequence'].create(seq)
        return res

    @api.multi
    def write(self, vals):
        # Update the prefix of the sequence if the 'internal_code_prefix' is
        #  changed, if there is not any sequence yet, create a new one.
        if 'internal_code_prefix' in vals:
            for rc in self:
                seq_code = rc.env['ir.sequence'].search([
                    ('code', '=', 'product.product.internal_code'),
                    ('company_id', '=', rc.id)
                ])
            if seq_code:
                seq_code[0].prefix = vals['internal_code_prefix']
            else:
                seq = {
                    'name': rc.name + ' - Product Sequence',
                    'code': 'product.product.internal_code',
                    'prefix': vals['internal_code_prefix'],
                    'padding': 5,
                    'number_increment': 1,
                    'company_id': rc.id,
                }
                self.env['ir.sequence'].create(seq)
        return super(ResCompany, self).write(vals)
