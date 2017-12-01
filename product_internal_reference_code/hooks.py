# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limted
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, SUPERUSER_ID


def _create_ir_sequence(cr, registry):
    # Create ir_sequence for current company
    env = api.Environment(cr, SUPERUSER_ID, {})
    company_list = env['res.company'].search([])
    for company in company_list:
        sequence = env['ir.sequence'].search([
            ('code', '=', 'product.product.internal_code'),
            ('company_id', '=', company.id)
        ])
        if not sequence:
            seq = {
                'name': company.name + ' - Product Sequence',
                'code': 'product.product.internal_code',
                'prefix': company.id,
                'padding': 5,
                'number_increment': 1,
                'company_id': company.id,
            }
            env['ir.sequence'].create(seq)
