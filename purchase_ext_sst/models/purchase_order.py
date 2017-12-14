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
    delivery_staff_id = fields.Many2one('hr.employee', 'Delivery Staff')
    worked_hours = fields.Selection(
        [(num/2, str(num/2) + ' hours') for num in range(1, 21)],
        string='Worked Hours',
    )

    @api.onchange('delivery_staff_id')
    def onchange_delivery_staff_id(self):
        if (not self.shop_id and self.delivery_staff_id) or \
            (self.shop_id and self.delivery_staff_id and \
                self.delivery_staff_id.shop_id != self.shop_id):
            self.shop_id = self.delivery_staff_id.shop_id

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
            if self.delivery_staff_id and self.delivery_staff_id.shop_id and \
                    self.delivery_staff_id.shop_id != self.shop_id:
                self.delivery_staff_id = False
        return {
            'domain': {'delivery_staff_id': ids}
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
