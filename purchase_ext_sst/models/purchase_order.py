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
    remark = fields.Char('Remark')
    call_back = fields.Boolean('Call Back')
    shop_id = fields.Many2one('res.shop', 'Shop')
    phone = fields.Char(related='partner_id.phone', store=True, readonly=True)
    address = fields.Char(
        related='partner_id.street',
        store=True,
        readonly=True,
        string='Address',
    )


    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        super(PurchaseOrder, self).onchange_partner_id()
        if not self.partner_id:
            self.shop_id = False
        else:
            self.shop_id = self.partner_id.shop_id
        return {}
