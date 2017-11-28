# -*- coding: utf-8 -*-
# OpenERP, Open Source Management Solution
# Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from odoo import models, api


class Product(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, vals):
        if not vals.get('default_code', False):
            internal_code_prefix = self.env.user.company_id.internal_code_prefix
            seq_code = self.env['ir.sequence'].next_by_code('product.product.internal_code')
            vals.update({'default_code': internal_code_prefix + seq_code})
        return super(Product, self).create(vals)