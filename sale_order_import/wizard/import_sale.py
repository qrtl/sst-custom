# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import csv
import io 
from tempfile import TemporaryFile
from datetime import datetime
import base64
from base64 import encodestring
from odoo.tools import pycompat

# import xlrd
import sys
import urllib

from odoo.exceptions import except_orm, Warning, RedirectWarning
from odoo import models, fields, api, _
from odoo import tools


class ImportSale(models.TransientModel):
    _name = 'import.sale'

    input_file = fields.Binary(
        'Sale Order File (.csv Format)',
        required=True,
    )
    datas_fname = fields.Char(
        'File Path'
    )
    picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        required=True,
        string='Shipping Policy',
        default=_get_picking_policy,
    )
    customer_invoice_journal_id = fields.Many2one(
        'account.journal',
        required=True,
        string='Customer Invoice Journal',
        default=_get_customer_invoice_journal_id,
    )
    customer_payment_journal_id = fields.Many2one(
        'account.journal',
        required=True,
        string='Customer Payment Journal',
        default=_get_customer_payment_journal_id,
    )

    @api.model
    def _get_picking_policy(self):
        default_rec = self.env['sale.import.default'].search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if default_rec:
            return default_rec.picking_policy

    @api.model
    def _get_customer_invoice_journal_id(self):
        default_rec = self.env['sale.import.default'].search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if default_rec:
            return default_rec.customer_invoice_journal_id

    @api.model
    def _get_customer_payment_journal_id(self):
        default_rec = self.env['sale.import.default'].search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if default_rec:
            return default_rec.customer_payment_journal_id

    @api.model
    def _get_partner_dict(self, partner_value, partner_dict, error_line_vals):
        if partner_value not in partner_dict.keys():
            partner = self.env['res.partner'].search([('name', '=', partner_value)])
            if not partner:
                error_line_vals['error_name'] = error_line_vals['error_name'] + _('Partner: ') + partner_value + _(' Not Found!') + '\n'
                error_line_vals['error'] = True
            else:
                partner_dict[partner_value] = partner.id

    @api.model
    def _get_product_dict(self, product_id_value, product_dict, error_line_vals):
        if product_id_value not in product_dict.keys():
            product = self.env['product.product'].search([('default_code', '=', product_id_value)])
            if not product:
                error_line_vals['error_name'] = error_line_vals['error_name'] + _('Product: ') + product_id_value + _(' Not Found!') + '\n'
                error_line_vals['error'] = True
            else:
                product_dict[product_id_value] = product.id

    @api.model
    def _get_pricelist_dict(self, pricelist_value, pricelist_dict, error_line_vals):
        if pricelist_value not in pricelist_dict.keys():
            pricelist = self.env['product.pricelist'].search([('name', '=', pricelist_value)])
            if not pricelist:
                error_line_vals['error_name'] = error_line_vals['error_name'] + _('Pricelist: ') + pricelist_value + _(' Not Found!') + '\n'
                error_line_vals['error'] = True
            else:
                pricelist_dict[pricelist_value] = pricelist.id

    @api.model
    def _get_picking_dict(self, warehouse_value, picking_dict, error_line_vals):
        warehouse_id = self.env['stock.warehouse'].search([('name','=',warehouse_value)]).id
        if not warehouse_id:
            error_line_vals['error_name'] = error_line_vals['error_name'] + _('Warehouse: ') + warehouse_value + _(' Not Found!') + '\n'
            error_line_vals['error'] = True
        else:
            picking_type = self.env['stock.picking.type'].search([('warehouse_id','=',warehouse_id),('code','=','outgoing')])
            picking_dict[warehouse_value] = picking_type

    @api.model
    def _get_taxes(self, tax_from_chunk, taxes, error_line_vals):
        tax_name_list = tax_from_chunk.split(',')
        for tax_name in tax_name_list:
            tax = self.env['account.tax'].search([('name', '=', tax_name)],
                                                 limit=1)
            if not tax:
                error_line_vals['error_name'] = error_line_vals['error_name'] + _('Tax: ') + tax_name + _(' Not Found!') + '\n'
                error_line_vals['error'] = True
            else:
                for taxdata in tax:
                    taxes.append(taxdata.id)

    @api.model
    def _check_csv_format(self, row):
        for r in row:
            try:
                r.decode('utf-8')
            except:
                raise Warning(_('Please prepare a CSV file with UTF-8 encoding.!'))

    @api.model
    def _update_error_log(self, error_log_id, error_line_vals, ir_attachment, model, row_no, order_group_value):
        if not error_log_id and error_line_vals['error']:
            error_log_id = self.env['error.log'].create({'input_file': ir_attachment.id,
                                                         'import_user_id' : self.env.user.id,
                                                        'import_date': datetime.now(),
                                                        'state': 'failed',
                                                        'model_id': model.id}).id
            error_line_id = self.env['error.log.line'].create({
                                        'row_no' : row_no,
                                        'order_group' : order_group_value,
                                        'error_name': error_line_vals['error_name'],
                                        'log_id' : error_log_id
                                    })
        elif error_line_vals['error']:
            error_line_id = self.env['error.log.line'].create({
                                        'row_no' : row_no,
                                        'order_group' : order_group_value,
                                        'error_name': error_line_vals['error_name'],
                                        'log_id' : error_log_id
                                    })
        return error_log_id

    @api.model
    def _get_order_id(self, order_data, item, error_log_id):
        order_vals = {
            'name' : 'New', #'/', # odoo11
            'partner_id' : order_data['partner_id'],
            'partner_invoice_id' : order_data['partner_invoice_id'],
            'pricelist_id' : order_data['pricelist_id'],
#             'location_id': order_data['location_id'], # odoo11
            'partner_shipping_id' : order_data['partner_shipping_id'],
            'payment_term_id': order_data['payment_term'],
            'state' : 'draft',
            'picking_policy': order_data['picking_policy'],
#             'currency_id' : order_data['currency_id'], # odoo11
            'note': order_data['note'],
            'error_log_id': error_log_id,
            'imported_order': True,
            'order_ref': item,
            
        }
        return self.env['sale.order'].create(order_vals)

    @api.model
    def _get_orderline_id(self, so_line, order_id):
        orderline_vals = {
            'name' : so_line['name'],
            'product_id' : so_line['product_id'],
            'product_uom_qty' : so_line['product_uom_qty'],
            'product_uom': so_line['product_uom'],
#             'invoiced' : False, # odoo11
            'price_unit' : so_line['price_unit'],
            'state' : so_line['state'],
            'tax_id': [(6, 0, so_line['tax_id'])],
            'order_id' : order_id.id,
        }
        return self.env['sale.order.line'].create(orderline_vals)


    @api.multi
    def import_sale_data(self):
#         if not self.customer_invoice_journal_id:
#             raise Warning(_('Error!'),_('Please select Customer Invoice Journal.'))
#         
#         if not self.customer_payment_journal_id:
#             raise Warning(_('Error!'),_('Please select Customer Payment Journal.'))
        for line in self:
#             try:
#                 lines = xlrd.open_workbook(file_contents=base64.decodestring(self.input_file))
#             except IOError as e:
#                 raise Warning(_('Import Error!'),_(e.strerror))
#             except ValueError as e:
#                 raise Warning(_('Import Error!'),_(e.strerror))
#             except:
#                 e = sys.exc_info()[0]
#                 raise Warning(_('Import Error!'),_('Wrong file format. Please enter .xlsx file.'))
#             if len(lines.sheet_names()) > 1:
#                 raise Warning(_('Import Error!'),_('Please check your xlsx file, it seems it contains more than one sheet.'))

            model = self.env['ir.model'].search([('model', '=', 'sale.order')])

            product_dict = {}
            partner_dict = {}
            pricelist_dict = {}
            order_item_dict = {}
            tax_dict = {}
            order_dict = {}
            picking_dict = {}
            error_log_id = False
            
            ir_attachment = self.env['ir.attachment'].create({'name': self.datas_fname,
                        'datas': self.input_file,
                        'datas_fname': self.datas_fname})
             
#             fileobj = TemporaryFile('w+')
#             fileobj.write(base64.b64decode(self.input_file))
#             fileobj.seek(0)
#             reader = csv.reader(fileobj)

            # new code to read csv
            csv_data = base64.decodestring(self.input_file)
            csv_iterator = pycompat.csv_reader(
                io.BytesIO(csv_data),
                quotechar='"',
                delimiter=','
            )
            fields = next(csv_iterator)

            order_group = fields.index('Group')
            partner_id = fields.index('Customer')
            product_id = fields.index('Line Product')
            line_name = fields.index('Line Description')
            price_unit = fields.index('Line Unit Price')
            product_qty = fields.index('Line Qty')
            taxes_id = fields.index('Line Tax')
            notes = fields.index('Notes')
            pricelist_id = fields.index('Pricelist')
            warehouse_id = fields.index('Warehouse')

#             line = 1
            for row in csv_iterator:
#                 line += 1

#                 if line == 1:#Get the index of header and skip the first line
#                     
#                     order_group = row.index('Group')
#                     partner_id = row.index('Customer')
#                     product_id = row.index('Line Product')
#                     line_name = row.index('Line Description')
#                     price_unit = row.index('Line Unit Price')
#                     product_qty = row.index('Line Qty')
#                     taxes_id = row.index('Line Tax')
#                     notes = row.index('Notes')
#                     pricelist_id = row.index('Pricelist')
#                     warehouse_id = row.index('Warehouse')
#                     continue

                check_list = []# Below logic for is row values are empty on all columns then skip that line.
                order_group_value = row[order_group].strip()
                if not bool(row[order_group].strip()):
                    for r in row:
                        if bool(r.strip()):
                            check_list.append(r)
                    if not bool(row[order_group].strip()) and not check_list:
                        continue

#                 if line == 2:#Check for UTF-8 Format. Only for first line i.e. line=2.
#                     self._check_csv_format(row)

                error_line_vals = {'error_name' : '', 'error': False}
                partner_value = row[partner_id].strip()
                if not partner_value:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Partner is empty!') + '\n'
                    error_line_vals['error'] = True
                else:
                    self._get_partner_dict(partner_value, partner_dict, error_line_vals)

                product_id_value = row[product_id].strip()
                if not product_id_value:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Product is empty!') + '\n'
                    error_line_vals['error'] = True
                else:
                    self._get_product_dict(product_id_value, product_dict, error_line_vals)

                pricelist_value = row[pricelist_id].strip()
                if not pricelist_value:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Pricelist is empty!') + '\n'
                    error_line_vals['error'] = True
                else:
                    self._get_pricelist_dict(pricelist_value, pricelist_dict, error_line_vals)

                warehouse_value = row[warehouse_id].strip()
                if not warehouse_value:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Warehouse is empty!') + '\n'
                    error_line_vals['error'] = True
                else:
                    self._get_picking_dict(warehouse_value, picking_dict, error_line_vals)

                taxes = []
                tax_from_chunk = row[taxes_id].strip()
                if tax_from_chunk:
                    self._get_taxes(tax_from_chunk, taxes, error_line_vals)

                qty = row[product_qty].strip()
                if not qty:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Quantity is empty!') + '\n'
                    error_line_vals['error'] = True
                else:
                    qty = float(qty)

                if qty <= 0:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Quantity not less than zero!') + '\n'
                    error_line_vals['error'] = True

                price_unit_value = row[price_unit].strip()
                if not price_unit_value:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Unit Price is empty!') + '\n'
                    error_line_vals['error'] = True
                else:
                    price_unit_value = float(price_unit_value)

                if price_unit_value <= 0:
                    error_line_vals['error_name'] = error_line_vals['error_name'] + _('Unit Price not less than zero!') + '\n'
                    error_line_vals['error'] = True

                picking_policy = self.picking_policy
                order = row[order_group].strip()

                error_log_id = self._update_error_log(error_log_id, error_line_vals, ir_attachment, model, line, order)

                if not error_log_id:
                    name = row[line_name].strip()
#                     product_data = self.env['sale.order.line'].product_id_change(pricelist_dict[pricelist_value], product_dict[product_id_value], qty, False, 0, False, '', partner_dict[partner_value],False, True, False, False, False, False)
#                     product_data = self.env['sale.order.line'].product_id_change()
                    product_data = self.env['product.product'].browse(product_dict[product_id_value]) # odoo11
                    if not name:
                        name = product_data['value']['name']

                    state = 'draft'
                    if order not in order_item_dict.keys():
                        order_item_dict[order] = [{
                                            'name' : name,
                                            'product_id' : product_dict[product_id_value],
                                            'product_uom_qty' : qty,
#                                             'product_uom' : product_data['value']['product_uom'], # odoo11
                                            'product_uom' : product_data.uom_id.id,
                                            'price_unit' : price_unit_value,
                                            'state' : state,
                                            'tax_id':taxes,
                                            }]
                    else:
                        order_item_dict[order].append({
                                            'name' : name,
                                            'product_id' : product_dict[product_id_value],
                                            'product_uom_qty' : qty,
#                                             'product_uom' : product_data['value']['product_uom'],# odoo11
                                            'product_uom' : product_data.uom_id.id,
                                            'price_unit' : price_unit_value,
                                            'state' : state,
                                            'tax_id':taxes,
                                            })

                    if order not in order_dict:
#                         pricelist_data = self.env['sale.order'].onchange_pricelist_id(pricelist_dict[pricelist_value], False)
#                         partner_data = self.env['sale.order'].onchange_partner_id(partner_dict[partner_value])
                        partner_data = self.env['res.partner'].browse(partner_dict[partner_value])
                        pricelist_data = partner_data.property_product_pricelist and partner_data.property_product_pricelist.id or False
                        addr = partner_data.address_get(['delivery', 'invoice'])
                        order_dict[order] = {
                                        'partner_id' : partner_dict[partner_value],
#                                         'partner_invoice_id' : partner_data['value']['partner_invoice_id'], # odoo11
                                        'partner_invoice_id' : addr['invoice'],
                                        'pricelist_id' : pricelist_dict[pricelist_value],
                                        'location_id': picking_dict[warehouse_value].default_location_dest_id and picking_dict[warehouse_value].default_location_dest_id.id,
#                                         'partner_shipping_id' : partner_data['value']['partner_shipping_id'], # odoo11
                                        'partner_shipping_id' : addr['delivery'],
#                                         'payment_term': partner_data['value']['payment_term'], # odoo11
                                        'payment_term':  partner_data.property_payment_term_id and partner_data.property_payment_term_id.id or False,
                                        'picking_policy': picking_policy,
#                                         'currency_id' : pricelist_data['value']['currency_id'], # odoo11
                                        'note': row[notes].strip()
                                        }
            if not error_log_id:
                error_log_id = self.env['error.log'].create({'input_file': ir_attachment.id,
                                                             'import_user_id' : self.env.user.id,
                                                             'import_date': datetime.now(),
                                                             'state': 'done',
                                                             'model_id': model.id}).id
                                                                
                for item in order_item_dict:
                    order_id = self._get_order_id(order_dict[item], item, error_log_id)
                    
                    for so_line in order_item_dict[item]:
                        orderline_id = self._get_orderline_id(so_line, order_id)

#                     order_id.signal_workflow('order_confirm') # odoo11
                    order_id.action_confirm() # odoo11
                    if order_id.picking_ids:
                        for picking in order_id.picking_ids:
                            available = picking.action_assign()

                    invoice_ids = order_id.action_invoice_create() # odoo11

                    if order_id.invoice_ids:
                        for invoice in order_id.invoice_ids:
                            invoice.journal_id = self.customer_invoice_journal_id.id
                            if invoice.state == 'draft':
#                                 invoice.signal_workflow('invoice_open')
                                invoice.action_invoice_open() # odoo11
                                invoice.pay_and_reconcile(self.customer_payment_journal_id.id) # odoo11

                                # no need to create manual payment we have odoo standard method to do this so just called it
#                                 if self.customer_payment_journal_id.currency and self.customer_payment_journal_id.currency.id != invoice.currency_id.id:
#                                     currency_id_voucher = self.customer_payment_journal_id.currency.id
#                                     voucher_amount = invoice.currency_id.compute(invoice.amount_total, self.customer_payment_journal_id.currency)
#                                 elif not self.customer_payment_journal_id.currency and invoice.currency_id.id != invoice.company_id.currency_id.id:
#                                     currency_id_voucher = invoice.company_id.currency_id.id
#                                     voucher_amount = invoice.currency_id.compute(invoice.amount_total, invoice.company_id.currency_id)
#                                 else:
#                                     currency_id_voucher = invoice.currency_id.id
#                                     voucher_amount = invoice.amount_total
#                                 partner_data  = self.env['account.voucher'].onchange_partner_id(invoice.partner_id.id,
#                                                                                                 self.customer_payment_journal_id.id,
#                                                                                                 voucher_amount,
#                                                                                                 currency_id_voucher,
#                                                                                                 'receipt',
#                                                                                                 invoice.date_invoice)
#                                 journal_data = self.env['account.voucher'].onchange_journal_voucher(line_ids= False,
#                                                                                                     tax_id=False,
#                                                                                                     price=0.0, 
#                                                                                                     partner_id=invoice.partner_id.id,
#                                                                                                     journal_id=self.customer_payment_journal_id.id,
#                                                                                                     ttype='receipt',
#                                                                                                     company_id=invoice.company_id.id)
#                                 line_cr_list = []
#                                 for line in partner_data['value']['line_cr_ids']:
#                                     moveline = self.env['account.move.line'].browse(line['move_line_id'])
#                                     if invoice.id == moveline.invoice.id:
#                                         line['amount'] = voucher_amount
#                                         line_cr_list.append((0, 0, line))
#                                         break #IF one line found then get out of loop since invoice and payment has one to one relation.
#                                 voucher_vals = {
#                                     'name': '/',
#                                     'partner_id' : invoice.partner_id.id,
#                                     'company_id' : invoice.company_id.id,
#                                     'journal_id' : self.customer_payment_journal_id.id,
#                                     'currency_id': currency_id_voucher,
#                                     'line_ids' : False,
#                                     'line_cr_ids' : line_cr_list,
#                                     'line_dr_ids' : False,
#                                     'account_id' : partner_data['value']['account_id'],
#                                     'period_id': journal_data['value']['period_id'],
#                                     'state': 'draft',
#                                     'date' : invoice.date_invoice,
#                                     'type': 'receipt',
#                                     'amount' : voucher_amount,
#                                     'payment_rate': journal_data['value']['payment_rate'],
#                                     'payment_rate_currency_id': journal_data['value']['payment_rate_currency_id']
#                                 }
#                                 voucher_id = self.env['account.voucher'].create(voucher_vals)
#                                 voucher_id.signal_workflow('proforma_voucher')
            res = self.env.ref('base_import_log.error_log_action')
            res = res.read()[0]
            res['domain'] = str([('id','in',[error_log_id])])
            return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
