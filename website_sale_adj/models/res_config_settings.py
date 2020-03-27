# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    property_payment_term_id = fields.Many2one(
        'account.payment.term',
        related='website_id.property_payment_term_id',
        string='Payment Term'
    )
