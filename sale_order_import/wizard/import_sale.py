# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import base64
from datetime import datetime
import io

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.tools import pycompat

FIELDS_TO_IMPORT = [
    'Group',
    'Customer',
    'Customer Phone/Mobile',
    'Line Product',
    'Line Description',
    'Line Unit Price',
    'Line Qty',
    'Line Tax',
    'Notes',
    'Pricelist',
    'Warehouse',
    'Team',
    'Carrier'
]


class ImportSale(models.TransientModel):
    _name = 'import.sale'

    @api.model
    def _default_picking_policy(self):
        """Get picking policy"""
        default_rec = self.env['sale.import.default'].search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if default_rec:
            return default_rec.picking_policy

    @api.model
    def _default_customer_invoice_journal(self):
        """Get customer invoice journal"""
        default_rec = self.env['sale.import.default'].search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if default_rec:
            return default_rec.customer_invoice_journal_id

    @api.model
    def _default_customer_payment_journal(self):
        """Get customer payment journal"""
        default_rec = self.env['sale.import.default'].search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if default_rec:
            return default_rec.customer_payment_journal_id

    input_file = fields.Binary(
        string='Sale Order File (.csv Format)',
        required=True,
    )
    datas_fname = fields.Char(
        string='File Path'
    )
    picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        string='Shipping Policy',
        required=True,
        default=_default_picking_policy,
    )
    customer_invoice_journal_id = fields.Many2one(
        'account.journal',
        string='Customer Invoice Journal',
        required=True,
        default=_default_customer_invoice_journal,
    )
    customer_payment_journal_id = fields.Many2one(
        'account.journal',
        string='Customer Payment Journal',
        required=True,
        default=_default_customer_payment_journal,
    )

    @api.model
    def _get_order_value_dict(self, row, error_line_vals, partner_tel,
                              product_id, pricelist_id, warehouse_id,
                              team_id, carrier_id, partner_dict, product_dict,
                              pricelist_dict, picking_dict, warehouse_dict,
                              team_dict, carrier_dict):
        """Get order value dict"""
        partner_value = row[partner_tel].strip()

        if not partner_value:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Customer Phone/Mobile" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            ctx = self._context.copy()

            partner_name_value = False
            if self._context.get('partner_name', False):
                partner_name_value = row[self._context['partner_name']].strip()
                ctx.update({'partner_name': partner_name_value})
            self.with_context(ctx)._get_partner_dict(partner_value,
                                                     partner_dict)

        product_id_value = row[product_id].strip()
        if not product_id_value:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Line Product" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            self._get_product_dict(product_id_value,
                                   product_dict, error_line_vals)

        pricelist_value = row[pricelist_id].strip()
        if not pricelist_value:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Pricelist" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            self._get_pricelist_dict(pricelist_value,
                                     pricelist_dict, error_line_vals)

        warehouse_value = row[warehouse_id].strip()
        if not warehouse_value:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Warehouse" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            self._get_picking_dict(warehouse_value, picking_dict,
                                   warehouse_dict, error_line_vals)

        team_value = row[team_id].strip()
        if not team_value:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Team" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            self._get_team_dict(team_value, team_dict, error_line_vals)

        carrier_value = row[carrier_id].strip()
        if not carrier_value:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Carrier" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            self._get_carrier_dict(carrier_value, carrier_dict,
                                   error_line_vals)

        return partner_value, product_id_value, pricelist_value,\
            warehouse_value, team_value, carrier_value

    @api.model
    def _get_order_value(self, row, error_line_vals, taxes, price_unit,
                         taxes_id, product_qty):
        """Get order value"""
        tax_from_chunk = row[taxes_id].strip()
        if tax_from_chunk:
            self._get_taxes(tax_from_chunk, taxes, error_line_vals)

        qty = row[product_qty].strip()
        if not qty:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Line Qty" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            try:
                qty = float(qty)
                if qty <= 0:
                    error_line_vals['error_name'] = error_line_vals[
                                                        'error_name'] + _(
                        'Column "Line Qty" must be greater than 0.') + '\n'
                    error_line_vals['error'] = True
            except ValueError:
                error_line_vals['error_name'] = error_line_vals['error_name'] \
                                                + _('Column "Line Qty" must '
                                                    'be a number.') + '\n'
                error_line_vals['error'] = True

        price_unit_value = row[price_unit].strip()
        if not price_unit_value:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Column "Line Unit Price" cannot be empty.') + '\n'
            error_line_vals['error'] = True
        else:
            try:
                price_unit_value = float(price_unit_value)
                if price_unit_value <= 0:
                    error_line_vals['error_name'] = error_line_vals[
                                                        'error_name'] + _(
                        'Column "Line Unit Price" must be greater than 0.') \
                                                    + '\n'
                    error_line_vals['error'] = True
            except ValueError:
                error_line_vals['error_name'] = error_line_vals['error_name'] \
                                                + _('Column "Line Unit '
                                                    'Price" must be a '
                                                    'number.') + '\n'
                error_line_vals['error'] = True
        return qty, price_unit_value

    @api.model
    def _get_order_item_dict(self, error_log_id, row, order, taxes, line_name,
                             product_dict, product_id_value, order_item_dict,
                             qty, price_unit_value):
        """Get order item dict"""
        if not error_log_id:
            name = row[line_name].strip()
            product_data = self.env['product.product'].browse(
                product_dict[product_id_value]
            )  # odoo11
            if not name:
                name = product_data.name

            invoiceable = True
            if product_data.invoice_policy == 'delivery':
                invoiceable = False

            state = 'draft'
            if order not in order_item_dict.keys():
                order_item_dict[order] = [{
                    'name': name,
                    'product_id': product_dict[product_id_value],
                    'product_uom_qty': qty,
                    #  'product_uom':
                    #  product_data['value']['product_uom'],  # odoo11
                    'product_uom': product_data.uom_id.id,
                    'price_unit': price_unit_value,
                    'state': state,
                    'tax_id':taxes,
                    'invoiceable': invoiceable,
                }]
            else:
                order_item_dict[order].append({
                    'name': name,
                    'product_id': product_dict[product_id_value],
                    'product_uom_qty': qty,
                    #  'product_uom':
                    #  product_data['value']['product_uom'],  # odoo11
                    'product_uom': product_data.uom_id.id,
                    'price_unit': price_unit_value,
                    'state': state,
                    'tax_id': taxes,
                    'invoiceable': invoiceable,
                })

    @api.model
    def _get_order_dict(self, error_log_id, order_dict, order, partner_dict,
                        partner_value, pricelist_dict, pricelist_value,
                        picking_dict, picking_policy, team_dict, team_value,
                        carrier_dict, carrier_value,
                        warehouse_dict, warehouse_value, row, notes):
        """Get order dict"""
        if not error_log_id:
            if order not in order_dict:
                partner_data = self.env['res.partner'].browse(
                    partner_dict[partner_value]
                )
                partner_data.property_product_pricelist and\
                    partner_data.property_product_pricelist.id or False
                addr = partner_data.address_get(['delivery', 'invoice'])
                order_dict[order] = {
                    'partner_id': partner_dict[partner_value],
                    #  'partner_invoice_id':
                    #  partner_data['value']['partner_invoice_id'], odoo11
                    'partner_invoice_id': addr['invoice'],
                    'pricelist_id': pricelist_dict[pricelist_value],
                    'location_id':
                    picking_dict[warehouse_value].default_location_dest_id
                    and
                    picking_dict[warehouse_value].default_location_dest_id.id,
                    #  'partner_shipping_id':
                    #  partner_data['value']['partner_shipping_id'],
                    #  odoo11
                    'partner_shipping_id': addr['delivery'],
                    #  'payment_term': partner_data['value']['payment_term'],
                    # odoo11
                    'payment_term':
                    partner_data.property_payment_term_id
                    and partner_data.property_payment_term_id.id
                    or False,
                    'picking_policy': picking_policy,
                    'team_id': team_dict[team_value],
                    'carrier_id': carrier_dict[carrier_value],
                    'warehouse_id': warehouse_dict[warehouse_value],
                    #  'currency_id':
                    #      pricelist_data['value']['currency_id'],  # odoo11
                    'note': row[notes].strip()}

    @api.model
    def _get_partner_dict(self, partner_value, partner_dict):
        """Get partner dict"""
        if partner_value not in partner_dict.keys():
#             partner = self.env['res.partner'].search(
#                 [('name', '=', partner_value),
#                  ('active', '=', True)])
            res_partner = self.env['res.partner']
            partner = res_partner.search(
                ['|', ('phone', '=', partner_value),
                 ('mobile', '=', partner_value),
                 ('active', '=', True)])
            if not partner:
                partner_name = self._context.get('partner_name', False)
                partner_id = res_partner.create({
                    'name': partner_name and partner_name or partner_value,
                    'phone': partner_value,
                    'mobile': partner_value,
                })
                partner_dict[partner_value] = partner_id.id
#                 error_line_vals['error_name'] =\
#                     error_line_vals['error_name']\
#                     + _('Partner: ') + partner_value + _(' Not Found!')\
#                     + '\n'
#                 error_line_vals['error'] = True
            else:
                #  pick the first partner that matches the domain
                #  fixme logic should be further refined
                partner_dict[partner_value] = partner[0].id

    @api.model
    def _get_product_dict(self, product_id_value, product_dict,
                          error_line_vals):
        """Get product dict"""
        if product_id_value not in product_dict.keys():
            product_product = self.env['product.product']
            product = product_product.search([
                ('default_code', '=', product_id_value)
            ])
            if not product:
                error_line_vals['error_name'] = error_line_vals['error_name']\
                    + _('Product: ') + product_id_value + _(' Not Found!')\
                    + '\n'
                error_line_vals['error'] = True
            else:
                product_dict[product_id_value] = product.id

    @api.model
    def _get_pricelist_dict(self, pricelist_value, pricelist_dict,
                            error_line_vals):
        """Get pricelist dict"""
        if pricelist_value not in pricelist_dict.keys():
            product_pricelist = self.env['product.pricelist']
            pricelist = product_pricelist.search([
                ('name', '=', pricelist_value)
            ])
            if not pricelist:
                error_line_vals['error_name'] = error_line_vals['error_name']\
                    + _('Pricelist: ') + pricelist_value + _(' Not Found!')\
                    + '\n'
                error_line_vals['error'] = True
            else:
                pricelist_dict[pricelist_value] = pricelist.id

    @api.model
    def _get_picking_dict(self, warehouse_value, picking_dict, warehouse_dict,
                          error_line_vals):
        """Get picking dict"""
        stock_warehouse = self.env['stock.warehouse']
        warehouse_id = stock_warehouse.search([
            ('name', '=', warehouse_value)]).id
        if not warehouse_id:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Warehouse: ') + warehouse_value + _(' Not Found!') + '\n'
            error_line_vals['error'] = True
        else:
            stock_picking_type = self.env['stock.picking.type']
            picking_type = stock_picking_type.search([
                ('warehouse_id', '=', warehouse_id),
                ('code', '=', 'outgoing')
            ])
            picking_dict[warehouse_value] = picking_type
            warehouse_dict[warehouse_value] = warehouse_id

    @api.model
    def _get_carrier_dict(self, carrier_value, carrier_dict, error_line_vals):
        """get carrier dict"""
        carrier_obj = self.env['delivery.carrier']
        carrier_id = carrier_obj.search([
            ('name', '=', carrier_value)])
        if not carrier_id:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Carrier: ') + carrier_value + _(' Not Found!') + '\n'
            error_line_vals['error'] = True
        else:
            #pick the first carrier that matches the domain
            carrier_dict[carrier_value] = carrier_id[0].id

    @api.model
    def _get_team_dict(self, team_value, team_dict, error_line_vals):
        """get team dict"""
        crm_team = self.env['crm.team']
        team_id = crm_team.search([
            ('name', '=', team_value)])
        if not team_id:
            error_line_vals['error_name'] = error_line_vals['error_name']\
                + _('Team: ') + team_value + _(' Not Found!') + '\n'
            error_line_vals['error'] = True
        else:
            #pick the first team that matches the domain
            team_dict[team_value] = team_id[0].id

    @api.model
    def _get_taxes(self, tax_from_chunk, taxes, error_line_vals):
        """Get taxes"""
        tax_name_list = tax_from_chunk.split(',')
        for tax_name in tax_name_list:
            tax = self.env['account.tax'].search([('name', '=', tax_name)],
                                                 limit=1)
            if not tax:
                error_line_vals['error_name'] = error_line_vals['error_name']\
                    + _('Tax: ') + tax_name + _(' Not Found!') + '\n'
                error_line_vals['error'] = True
            else:
                for taxdata in tax:
                    taxes.append(taxdata.id)

    @api.model
    def _check_csv_format(self, row):
        """Check csv format"""
        for r in row:
            try:
                r.decode('utf-8')
            except:
                raise Warning(_(
                    'Please prepare a CSV file with UTF-8 encoding.!'
                ))

    @api.model
    def _update_error_log(self, error_log_id, error_line_vals, ir_attachment,
                          model, row_no, order_group_value):
        """Update error log"""
        error_line = self.env['error.log.line']
        if not error_log_id and error_line_vals['error']:
            error_log = self.env['error.log']
            error_log_id = error_log.create({'input_file': ir_attachment.id,
                                            'import_user_id': self.env.user.id,
                                            'import_date': datetime.now(),
                                            'state': 'failed',
                                            'model_id': model.id}).id
            error_line.create({
                'row_no': row_no,
                'order_group': order_group_value,
                'error_name': error_line_vals['error_name'],
                'log_id': error_log_id})
        elif error_line_vals['error']:
            error_line.create({
                'row_no': row_no,
                'order_group': order_group_value,
                'error_name': error_line_vals['error_name'],
                'log_id': error_log_id})
        return error_log_id

    @api.model
    def _get_order_id(self, order_data, item, error_log_id):
        """Get order id"""
        order_vals = {
            # 'name': 'New', #'/', # odoo11
            'partner_id': order_data['partner_id'],
            'partner_invoice_id': order_data['partner_invoice_id'],
            'pricelist_id': order_data['pricelist_id'],
            #  'location_id': order_data['location_id'], # odoo11
            'partner_shipping_id': order_data['partner_shipping_id'],
            'payment_term_id': order_data['payment_term'],
            'state': 'draft',
            'picking_policy': order_data['picking_policy'],
            #  'currency_id': order_data['currency_id'],  # odoo11
            'note': order_data['note'],
            'error_log_id': error_log_id,
            'imported_order': True,
            'order_ref': item,
            'team_id': order_data['team_id'],
            'warehouse_id': order_data['warehouse_id'],
            'carrier_id': order_data['carrier_id'],
            }
        return self.env['sale.order'].create(order_vals)

    @api.model
    def _get_orderline_id(self, so_line, order_id):
        """Get order line id"""
        orderline_vals = {'name': so_line['name'],
                          'product_id': so_line['product_id'],
                          'product_uom_qty': so_line['product_uom_qty'],
                          'product_uom': so_line['product_uom'],
                          #  'invoiced': False,  # odoo11
                          'price_unit': so_line['price_unit'],
                          'state': so_line['state'],
                          'tax_id': [(6, 0, so_line['tax_id'])],
                          'order_id': order_id.id}
        return self.env['sale.order.line'].create(orderline_vals)

    def import_sale_data(self):
        self.ensure_one()
        ctx = self._context.copy()
        model = self.env['ir.model'].search([('model', '=', 'sale.order')])

        product_dict = {}
        partner_dict = {}
        pricelist_dict = {}
        order_item_dict = {}
        #  tax_dict = {}
        order_dict = {}
        picking_dict = {}
        warehouse_dict = {}
        team_dict = {}
        carrier_dict = {}
        error_log_id = False
        ir_attachment_obj = self.env['ir.attachment']
        ir_attachment = ir_attachment_obj.create({
            'name': self.datas_fname,
            'datas': self.input_file,
            'datas_fname': self.datas_fname
        })

        # new code to read csv
        # csv_data = base64.decodestring(self.input_file)
        csv_data = base64.decodebytes(self.input_file)
        csv_iterator = pycompat.csv_reader(
            io.BytesIO(csv_data),
            quotechar='"',
            delimiter=','
        )
        try:
            sheet_fields = next(csv_iterator)
        except:
            raise Warning(_("Please import a CSV file with UTF-8 encoding."))

        #  column validation
        missing_columns = list(set(FIELDS_TO_IMPORT) - set(sheet_fields))
        if missing_columns:
            raise Warning(
                _('Following columns are missing: \n %s'
                  % ('\n'.join(missing_columns))
                  )
            )

        order_group = sheet_fields.index('Group')
        missing_columns.append('Group')
        partner_name = sheet_fields.index('Customer')
        partner_tel = sheet_fields.index('Customer Phone/Mobile')
        product_id = sheet_fields.index('Line Product')
        line_name = sheet_fields.index('Line Description')
        price_unit = sheet_fields.index('Line Unit Price')
        product_qty = sheet_fields.index('Line Qty')
        taxes_id = sheet_fields.index('Line Tax')
        notes = sheet_fields.index('Notes')
        pricelist_id = sheet_fields.index('Pricelist')
        warehouse_id = sheet_fields.index('Warehouse')
        team_id = sheet_fields.index('Team')
        carrier_id = sheet_fields.index('Carrier')

        for row in csv_iterator:
            check_list = []
# Below logic for is row values are empty on all columns then skip that line.
#                 order_group_value = row[order_group].strip()
            if not bool(row[order_group].strip()):
                for r in row:
                    if bool(r.strip()):
                        check_list.append(r)
                if not bool(row[order_group].strip()) and not check_list:
                    continue

            error_line_vals = {'error_name': '', 'error': False}
            ctx.update({'partner_name': partner_name})
            partner_value, product_id_value, pricelist_value,\
                warehouse_value, team_value, carrier_value = \
                self.with_context(ctx)._get_order_value_dict(
                    row, error_line_vals, partner_tel, product_id,
                    pricelist_id, warehouse_id, team_id, carrier_id,
                    partner_dict,
                    product_dict, pricelist_dict, picking_dict,
                    warehouse_dict, team_dict, carrier_dict)

            taxes = []
            qty, price_unit_value = self._get_order_value(row,
                                                          error_line_vals,
                                                          taxes,
                                                          price_unit,
                                                          taxes_id,
                                                          product_qty)
            picking_policy = self.picking_policy
            order = row[order_group].strip()
            error_log_id = self._update_error_log(error_log_id,
                                                  error_line_vals,
                                                  ir_attachment, model,
                                                  csv_iterator.line_num,
                                                  order)

            self._get_order_item_dict(error_log_id, row, order, taxes,
                                      line_name, product_dict,
                                      product_id_value, order_item_dict,
                                      qty, price_unit_value)

            self._get_order_dict(error_log_id, order_dict, order,
                                 partner_dict, partner_value,
                                 pricelist_dict,
                                 pricelist_value, picking_dict,
                                 picking_policy, team_dict, team_value,
                                 carrier_dict, carrier_value,
                                 warehouse_dict, warehouse_value, row,
                                 notes)

        if not error_log_id:
            error_log_id = self.env['error.log'].create({
                'input_file': ir_attachment.id,
                'import_user_id': self.env.user.id,
                'import_date': datetime.now(),
                'state': 'done',
                'model_id': model.id}).id
            for item in order_item_dict:
                order_id = self._get_order_id(order_dict[item],
                                              item, error_log_id)
                for so_line in order_item_dict[item]:
                    if not so_line['invoiceable']:
                        order_id.invoiceable = False
                    self._get_orderline_id(so_line, order_id)
#                         orderline_id = \
#                             self._get_orderline_id(so_line, order_id)

#                   order_id.signal_workflow('order_confirm')  # odoo11
                order_id.action_confirm()  # odoo11
                if order_id.picking_ids:
                    for picking in order_id.picking_ids:
                        picking.action_assign()
                        #  available = picking.action_assign()

                #  invoice_ids = order_id.action_invoice_create()  # odoo11
                if order_id.invoiceable:
                    order_id.action_invoice_create()  # odoo11

                if order_id.invoice_ids:
                    for invoice in order_id.invoice_ids:
                        invoice.journal_id = \
                            self.customer_invoice_journal_id.id
                        if invoice.state == 'draft':
#                                 invoice.signal_workflow('invoice_open')
                            invoice.action_invoice_open()  # odoo11
                            invoice.pay_and_reconcile(
                                self.customer_payment_journal_id.id
                            )  # odoo11
        res = self.env.ref('base_import_log.error_log_action')
        res = res.read()[0]
        res['domain'] = str([('id', 'in', [error_log_id])])
        return res
