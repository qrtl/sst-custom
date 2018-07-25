# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    member_group_id = fields.Many2one(
        'member.group',
        string='Member Group',
    )
    remaining_point_limit = fields.Integer(
        string='Available Points',
        compute='_compute_remaining_point_limit',
    )

    @api.multi
    def _compute_remaining_point_limit(self):
        for partner in self:
            subscribe_category_ids = partner.env['mail.followers'].search([
                ('partner_id', '=', partner.id),
                ('res_model', '=', 'product.public.category'),
            ])
            category_id_list = []
            for category_id in subscribe_category_ids:
                category_id_list.append(category_id.res_id)
            subscribe_category_list = partner.env[
                'product.public.category'].search([
                ('child_id', '=', False),
                ('id', 'in', category_id_list)
            ])
            subscribe_count = 0
            partner.remaining_point_limit = 0
            for subscribe_category in subscribe_category_list:
                subscribe_count += subscribe_category.subscribe_point
            if partner.member_group_id:
                partner.remaining_point_limit = \
                    partner.member_group_id.point_limit - subscribe_count
