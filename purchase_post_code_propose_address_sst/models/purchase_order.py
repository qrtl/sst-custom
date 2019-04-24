# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import jaconv
import json
import urllib

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    country_id = fields.Many2one(
        string='Country',
        default=lambda self: self.env.ref('base.jp')
    )
    state_id = fields.Many2one(
        'res.country.state',
        string='Prefecture',
    )
    city = fields.Char(
        string='City',
    )
    street = fields.Char(
        oldname='address',
        string='Street',
    )
    street2 = fields.Char(
        string='Street2',
    )
    zipcode = fields.Char(
        string='Post Code (Search)',
    )
    zip = fields.Char(
        related='partner_id.zip',
        string='Post Code (Supplier)',
        store=True,
        readonly=True,
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.state_id = self.partner_id.state_id
            self.city = self.partner_id.city
            self.street = self.partner_id.street
            self.street2 = self.partner_id.street2

    @api.onchange('zipcode')
    def _onchange_zipcode(self):
        if self.zipcode:
            self.zipcode, msg = self.check_zipcode(self.zipcode)
            if not self.zipcode:
                return msg
            request_url = 'http://zipcloud.ibsnet.co.jp/api/search?zipcode' \
                          '=%s' % self.zipcode
            request = urllib.request.Request(request_url)
            response_data = json.loads(
                urllib.request.urlopen(request).read().decode('utf-8'))
            self.state_id = False
            self.city = False
            self.street = False
            self.street2 = False
            if response_data['status'] != 200:
                self.zipcode = False
                return {
                    'warning': {
                        'title': _("Error"),
                        'message': response_data['message']
                    }
                }
            else:
                address_data = response_data['results']
                if address_data:
                    self.state_id = self.env['res.country.state'].search([
                        ('name', '=', address_data[0]['address1'])
                    ], limit=1)
                    self.city = address_data[0]['address2']
                    self.street = address_data[0]['address3']

    def check_zipcode(self, zipcode):
        msg = {}
        field = jaconv.z2h(zipcode, ascii=True, digit=True).replace("-", "")
        if not field.isdigit():
            field = False
            msg = {
                'warning': {
                    'title': _("Error"),
                    'message': _("Only digits are allowed.")
                }
            }
        if len(field) != 7:
            field = False
            msg = {
                'warning': {
                    'title': _("Error"),
                    'message': _("Post code should be 7 digits.")
                }
            }
        return field, msg

    @api.multi
    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        for order in self:
            if not self.is_default_partner(order.partner_id.id) and \
                    order.zipcode and not order.partner_id.zip:
                order.partner_id.zip = order.zipcode
                order.partner_id.state_id = order.state_id
                order.partner_id.city = order.city
                order.partner_id.street = order.street
                order.partner_id.street2 = order.street2
        return res

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        if not self.is_default_partner(res.partner_id.id) and res.zipcode and \
                not res.partner_id.zip:
            res.partner_id.zip = res.zipcode
            res.partner_id.state_id = res.state_id
            res.partner_id.city = res.city
            res.partner_id.street = res.street
            res.partner_id.street2 = res.street2
        return res
