# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.account.controllers.portal import PortalAccount


class PortalAccount(PortalAccount):

    # Overwrite standard method, only invoices that the customer is related
    # to the user will be shown.
    def _get_account_invoice_domain(self):
        partner = request.env.user.partner_id
        domain = [
            ("type", "in", ["out_invoice", "out_refund"]),
            # ('message_partner_ids', 'child_of',
            # [partner.commercial_partner_id.id]),
            ("partner_id", "child_of", [partner.commercial_partner_id.id]),
            ("state", "in", ["open", "paid", "cancel"]),
        ]
        return domain
