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

from openerp import models, fields, api, _


class error_log_lines(models.Model):
    _name = 'error.log.line'

    error_name =  fields.Text('Error')
    row_no = fields.Integer('Row Number')
    order_group = fields.Char('Order Group')
    log_id = fields.Many2one('error.log', string='Log')
    
class error_log(models.Model):
    _name = 'error.log'
    
    _rec_name = 'model_id'
    
    import_date = fields.Datetime('Imported On')
    import_user_id = fields.Many2one('res.users', 'Imported By')
    log_line_ids = fields.One2many('error.log.line', 'log_id', string='Log Lines')
    input_file = fields.Many2one('ir.attachment', string='File')
    file_path = fields.Binary(related='input_file.datas',string='Imported File')
    file_name = fields.Char(related='input_file.datas_fname',string='File')
    state = fields.Selection([('done', 'Succeed'), ('failed', 'Failed')], string='Status')
    model_id = fields.Many2one('ir.model', string= 'Model')
    model_name = fields.Char(related='model_id.model', string='Model Name')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
