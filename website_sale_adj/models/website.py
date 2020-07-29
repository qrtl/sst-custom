# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    property_payment_term_id = fields.Many2one(
        "account.payment.term",
        company_dependent=True,
        string="Customer Payment Terms",
        help="This payment term will be applied to eCommerce orders if there "
        "is no payment term in customer",
    )

    @api.model
    def sale_get_payment_term(self, partner):
        DEFAULT_PAYMENT_TERM = "account.account_payment_term_immediate"
        return (
            partner.property_payment_term_id.id
            or request.website.property_payment_term_id.id
            or self.env.ref(DEFAULT_PAYMENT_TERM, False).id
        )
