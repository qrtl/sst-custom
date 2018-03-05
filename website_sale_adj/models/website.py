# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    property_payment_term_id = fields.Many2one(
        'account.payment.term',
        company_dependent=True,
        string='Customer Payment Terms',
        help="This payment term will be applied to eCommerce orders if there "
             "is no payment term in customer",
    )
