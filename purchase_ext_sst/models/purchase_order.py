# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    request_channel_id = fields.Many2one('request.channel', "Request Channel")
    request_medium_id = fields.Many2one('request.medium', "Request Medium")
    employee_id = fields.Many2one('hr.employee', "Received By")
    purchase_category_id = fields.Many2one(
        'purchase.category',
        "Purchase Category",
    )
    call_back = fields.Boolean('Call Back')
    shop_id = fields.Many2one('stock.warehouse', 'Shop')
    phone = fields.Char(index=True)
    phone2 = fields.Char(related='partner_id.mobile', index=True)
    tentative_name = fields.Char('Tentative Name', index=True)
    address = fields.Char()
    remark = fields.Text('Remark')
    purchased_by_id = fields.Many2one('hr.employee', 'Delivery Staff')
    worked_hours = fields.Selection(
        [(num, num + ' hours') for num in ['0.5', '1.0', '1.5', '2.0',
                                           '2.5', '3.0', '3.5', '4.0',
                                           '4.5', '5.0', '5.5', '6.0',
                                           '6.5', '7.0', '7.5', '8.0',
                                           '8.5', '9.0', '9.5', '10.0']],
        string='Worked Hours',
    )
    supplier_update_lock = fields.Boolean(
        'Supplier Update Lock',
        default=False,
    )

    @api.onchange('purchased_by_id')
    def onchange_purchased_by_id(self):
        if (not self.shop_id and self.purchased_by_id) or \
                (self.shop_id and self.purchased_by_id and \
                             self.purchased_by_id.shop_id != self.shop_id):
            self.shop_id = self.purchased_by_id.shop_id

    @api.onchange('shop_id')
    def onchange_shop_id(self):
        ids = []
        if self.shop_id:
            # Update domain filter on delivery staff
            staffs = self.env['hr.employee'].search([
                ('shop_id', '=', self.shop_id.id)
            ])
            ids.append(('id', 'in', staffs.ids))
            # Clear the delivery staff value
            if self.purchased_by_id and self.purchased_by_id.shop_id and \
                            self.purchased_by_id.shop_id != self.shop_id:
                self.purchased_by_id = False
            # Update picking_type_id
            picking_type_id = self.env['stock.picking.type'].search([
                ('code', '=', 'incoming'),
                ('warehouse_id', '=', self.shop_id.id),
                ('warehouse_id.company_id', 'in', [self.env.context.get(
                    'company_id', self.env.user.company_id.id),
                    False]),
            ], limit=1)
            if picking_type_id:
                self.picking_type_id = picking_type_id
        return {
            'domain': {'purchased_by_id': ids}
        }

    @api.multi
    def open_record(self):
        form_id = self.env.ref('purchase.purchase_order_form')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {},
            'target': 'current',
        }

    @api.multi
    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        for purchase_order in self:
            if not purchase_order.supplier_update_lock:
                if 'phone' in vals and vals['phone'] and \
                        self.is_default_partner(self.partner_id.id):
                    purchase_order.partner_id = self.get_purchase_order_partner(
                        vals)
                if not self.is_default_partner(self.partner_id.id) and \
                        'tentative_name' in vals and vals['tentative_name']:
                    purchase_order.partner_id.name = vals['tentative_name']
            for order_line in purchase_order.order_line:
                product = order_line.product_id.product_tmpl_id
                if product.shop_id != purchase_order.shop_id:
                    product.shop_id = purchase_order.shop_id
                if product.purchased_by_id != purchase_order.purchased_by_id:
                    product.purchased_by_id = purchase_order.purchased_by_id
        return res

    @api.model
    def create(self, vals):
        if 'phone' in vals and vals['phone'] and self.is_default_partner(
                vals['partner_id']):
            vals['partner_id'] = self.get_purchase_order_partner(vals)
        if not self.is_default_partner(vals['partner_id']) and \
                        'tentative_name' in vals and \
                        vals['tentative_name'] != '未確認':
            if not ('supplier_update_lock' in vals and vals[
                'supplier_update_lock']):
                self.env['res.partner'].browse(vals['partner_id']).name = \
                    vals['tentative_name']
        return super(PurchaseOrder, self).create(vals)

    def get_purchase_order_partner(self, vals):
        phone = vals['phone'] if 'phone' in vals else False
        partners = False
        if phone:
            partners = self.env['res.partner'].search([
                '|',
                ('mobile', '=', phone),
                ('phone', '=', phone),
            ])
        if not partners:
            if 'tentative_name' in vals and vals['tentative_name']:
                name = vals['tentative_name']
            else:
                name = '未確認'
            new_partner = self.env['res.partner'].create({
                'name': name,
                'phone': phone,
                'supplier': True,
                'customer': False,
            })
            return new_partner.id
        elif partners:
            return partners[0].id

    def is_default_partner(self, partner_id):
        company_id = self.env.user.company_id.id
        default_partner_id = (self.env['ir.default'].get('purchase.order',
                                                         'partner_id',
                                                         user_id=self.env.uid,
                                                         company_id=company_id) or
                              self.env['ir.default'].get('purchase.order',
                                                         'partner_id',
                                                         user_id=False,
                                                         company_id=company_id)) or False
        return partner_id == default_partner_id
