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
    phone = fields.Char(index=True)
    mobile = fields.Char(index=True)
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
        res = super(PurchaseOrder, self).write(vals)
        val_phone = 'phone' in vals and vals['phone'] or False
        val_mobile = 'mobile' in vals and vals['mobile'] or False
        val_tent_name = 'tentative_name' in vals and vals['tentative_name'] \
                         or False
        for order in self:
            phone = val_phone or order.phone
            mobile = val_mobile or order.mobile
            tent_name = val_tent_name or order.tentative_name
            if self.is_default_partner(order.partner_id.id):
                if val_phone or val_mobile:
                    partner_e = self.get_partner_from_phone(phone, mobile)
                    if partner_e and order.partner_id != partner_e:
                        self.set_particulars_from_partner(partner_e, phone,
                                                          mobile)
                    if not partner_e:
                        order.partner_id = self.create_partner(phone, mobile)
                    self.update_partner(order.partner_id, phone, mobile,
                                        tent_name)
            else:
                if val_phone or val_mobile or val_tent_name:
                    partner_e = self.get_partner_from_phone(phone,
                                                            mobile)
                    if partner_e and order.partner_id != partner_e:
                        self.update_partner(partner_e, phone, mobile,
                                            tent_name)
                        self.set_particulars_from_partner(partner_e, phone,
                                                          mobile)
                    else:
                        self.update_partner(order.partner_id, phone, mobile,
                                            tent_name)

            if 'order_line' in vals:
                for line in order.order_line:
                    product = line.product_id
                    if product.shop_id != order.shop_id:
                        product.shop_id = order.shop_id
                    if product.purchased_by_id != order.purchased_by_id:
                        product.purchased_by_id = order.purchased_by_id
        return res

    @api.model
    def create(self, vals):
        val_phone = 'phone' in vals and vals['phone'] or False
        val_mobile = 'mobile' in vals and vals['mobile'] or False
        val_tent_name = 'tentative_name' in vals and vals['tentative_name'] \
                         or False
        if self.is_default_partner(vals['partner_id']):
            if val_phone or val_mobile:
                partner_e = self.get_partner_from_phone(val_phone, val_mobile)
                if partner_e and vals['partner_id'] != partner_e.id:
                    vals['partner_id'] = partner_e.id
                    if not vals['phone']:
                        vals['phone'] = partner_e.phone
                    if not vals['mobile']:
                        vals['mobile'] = partner_e.mobile
                if not partner_e:
                    vals['partner_id'] = self.create_partner(val_phone,
                                                             val_mobile).id
                partner = self.env['res.partner'].browse(vals['partner_id'])
                self.update_partner(partner, val_phone, val_mobile,
                                    val_tent_name)
        else:
            if val_phone or val_mobile:
                partner_e = self.get_partner_from_phone(val_phone, val_mobile)
                if partner_e and vals['partner_id'] != partner_e.id:
                    vals['partner_id'] = partner_e.id
                partner = self.env['res.partner'].browse(vals['partner_id'])
                self.update_partner(partner, val_phone, val_mobile,
                                    val_tent_name)
        return super(PurchaseOrder, self).create(vals)

    def get_partner_from_phone(self, phone, mobile):
        Partner = self.env['res.partner']
        if phone and mobile:
            # here we use "or" condition instead of "and"
            partners = Partner.search([
                '|', ('phone', '=', phone), ('mobile', '=', mobile),
                ('supplier', '=', True)])
        elif phone:
            partners = Partner.search([
                ('phone', '=', phone), ('supplier', '=', True)])
        elif mobile:
            partners = Partner.search([
                ('mobile', '=', mobile), ('supplier', '=', True)])
        if partners and len(partners) > 1:
            conflicts_users_list = ''
            for partner in partners:
                conflicts_users_list += _('\n%s\n- Phone: %s\n- '
                                          'Mobile: %s\n') % (
                    partner.name,
                    partner.phone,
                    partner.mobile
                )
            raise UserError(_('The entered phone(%s) / mobile(%s) '
                              'conflicts with the following user(s):\n%s') %
                            (phone or 'N/A', mobile or 'N/A',
                             conflicts_users_list))
        return partners if partners else False

    def set_particulars_from_partner(self, partner, phone, mobile):
        self.partner_id = partner
        if not phone:
            self.phone = partner.phone
        if not mobile:
            self.mobile = partner.mobile

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
