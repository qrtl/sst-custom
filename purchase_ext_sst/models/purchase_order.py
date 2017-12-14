# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
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
    address = fields.Char()
    remark = fields.Text('Remark')
    delivery_staff = fields.Many2one('res.partner', 'Delivery Staff')
    worked_hours = fields.Selection(
        [(0.5, '30 minutes'),
         (1, '1 hour'),
         (1.5, '1.5 hours'),
         (2, '2 hours'),
         (2.5, '2.5 hours'),
         (3, '3 hours'),
         (3.5, '3.5 hours'),
         (4, '4 hours'),
         (4.5, '4.5 hours'),
         (5, '5 hours'),
         (5.5, '5.5 hours'),
         (6, '6 hours'),
         (6.5, '6.5 hours'),
         (7, '7 hours'),
         (7.5, '7.5 hours'),
         (8, '8 hours'),
         (8.5, '8.5 hours'),
         (9, '9 hours'),
         (9.5, '9.5 hours'),
         (10, '10 hours'),],
        string='Worked Hours'
    )

    @api.onchange('delivery_staff')
    def onchange_delivery_staff(self):
        if (not self.shop_id and self.delivery_staff) or \
            (self.shop_id and self.delivery_staff and \
                self.delivery_staff.shop_id != self.shop_id):
            self.shop_id = self.delivery_staff.shop_id
        return {}

    @api.onchange('shop_id')
    def onchange_shop_id(self):
        ids = []
        if self.shop_id:
            # Update domain filter on delivery staff
            staffs = self.env['res.partner'].search([
                ('shop_id', '=', self.shop_id.id)
            ])
            ids.append(('id', 'in', staffs.ids))
            # Clear the delivery staff value
            if self.delivery_staff and self.delivery_staff.shop_id and \
                    self.delivery_staff.shop_id != self.shop_id:
                self.delivery_staff = False
        return {
            'domain': {'delivery_staff': ids}
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
