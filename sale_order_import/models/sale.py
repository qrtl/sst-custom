# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp import models, api, _, fields

class error_log(models.Model):
    _inherit = 'error.log'

    sale_order_ids = fields.One2many('sale.order', 'error_log_id', string='Related Sale Orders')


class sale_order(models.Model):
    _inherit = 'sale.order'

    imported_order = fields.Boolean('Imported Order?', readonly=True)
    order_ref = fields.Char('Order Reference', readonly=True)
    error_log_id = fields.Many2one(relation='error.log', string='Import Log', readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
