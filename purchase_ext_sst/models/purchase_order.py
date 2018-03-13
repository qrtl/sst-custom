# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


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
    phone_update = fields.Char(index=True)
    mobile_update = fields.Char(index=True)
    phone_search = fields.Char(index=True)
    supplier_phone = fields.Char(
        related='partner_id.phone',
        string='Supplier Phone',
        readonly=True,
    )
    supplier_mobile = fields.Char(
        related='partner_id.mobile',
        string='Supplier Mobile',
        readonly=True,
    )
    tentative_name = fields.Char('Tentative Name')
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
        for order in self:
            val_phone_search = 'phone_search' in vals and vals[
                'phone_search'] or False
            val_phone = 'phone_update' in vals and vals['phone_update'] or \
                        val_phone_search or False
            val_mobile = 'mobile_update' in vals and vals['mobile_update'] \
                         or False
            val_tent_name = 'tentative_name' in vals and vals[
                'tentative_name'] or order.tentative_name
            vals['partner_id'] = 'partner_id' in vals and vals['partner_id']\
                                 or order.partner_id.id
            partner = self.get_partner_from_phone(val_phone, val_mobile)
            if self.is_default_partner(vals['partner_id']):
                if partner:
                    vals['partner_id'] = partner.id
                elif val_phone or val_mobile:
                    vals['partner_id'] = self.create_partner(val_phone,
                                                             val_mobile).id
            if not self.is_default_partner(vals['partner_id']):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                self.update_partner(partner, val_phone, val_mobile,
                                    val_tent_name)
        vals['phone_update'] = vals['mobile_update'] = vals['phone_search'] \
            = False
        return super(PurchaseOrder, self).write(vals)

    @api.model
    def create(self, vals):
        val_phone_search = 'phone_search' in vals and vals['phone_search'] \
                           or False
        val_phone = 'phone_update' in vals and vals['phone_update'] or \
                    val_phone_search or False
        val_mobile = 'mobile_update' in vals and vals['mobile_update'] or False
        val_tent_name = 'tentative_name' in vals and vals['tentative_name'] \
                         or False
        partner = self.get_partner_from_phone(val_phone, val_mobile)
        if self.is_default_partner(vals['partner_id']):
            if partner:
                vals['partner_id'] = partner.id
            elif val_phone or val_mobile:
                vals['partner_id'] = self.create_partner(val_phone,
                                                         val_mobile).id
        if not self.is_default_partner(vals['partner_id']):
            partner = self.env['res.partner'].browse(vals['partner_id'])
            self.update_partner(partner, val_phone, val_mobile, val_tent_name)
        vals['phone_update'] = vals['mobile_update'] = vals['phone_search'] \
            = False
        return super(PurchaseOrder, self).create(vals)

    @api.onchange('phone_search')
    def onchange_phone_search(self):
        if self.phone_search and self.partner_id and \
                self.is_default_partner(self.partner_id.id):
            partner = self.get_partner_from_phone(self.phone_search)
            if partner:
                self.partner_id = partner
                self.phone_update = False
                self.mobile_update = False
            else:
                self.phone_update = self.phone_search

    def get_partner_from_phone(self, *phones):
        Partner = self.env['res.partner']
        phone_list = []
        partners = False
        for phone in phones:
            if phone:
                phone_list.append(phone)
        # here we use "or" condition instead of "and"
        if phone_list:
            partners = Partner.search([
                '|',
                ('phone', 'in', list(phone_list)),
                ('mobile', 'in', list(phone_list)),
                ('supplier', '=', True)])
        if partners and len(partners) > 1:
            conflicts_users_list = ''
            for partner in partners:
                conflicts_users_list += _('\n%s\n- Phone: %s\n- '
                                          'Mobile: %s\n') % (
                    partner.name,
                    partner.phone,
                    partner.mobile
                )
            raise UserError(_('The entered phone (%s) '
                              'conflicts with the following user(s):\n%s') %
                            (','.join(list(phone_list)) or 'N/A',
                             conflicts_users_list))
        return partners if partners else False

    def create_partner(self, phone, mobile):
        partner = self.env['res.partner'].create({
            'name': '未確認',
            'phone': phone,
            'mobile': mobile,
            'supplier': True,
            'customer': False,
        })
        return partner

    def update_partner(self, partner, phone, mobile, tent_name):
        if phone and partner.phone != phone:
            partner.phone = phone
        if mobile and partner.mobile != mobile:
            partner.mobile = mobile
        if tent_name and partner.name != tent_name:
            partner.name = tent_name

    def is_default_partner(self, partner_id):
        company_id = self.env.user.company_id.id
        default_id = self.env['ir.default'].get('purchase.order',
                                                'partner_id',
                                                user_id=self.env.uid,
                                                company_id=company_id) or \
                     self.env['ir.default'].get('purchase.order',
                                                'partner_id',
                                                user_id=False,
                                                company_id=company_id) or False
        return partner_id == default_id
