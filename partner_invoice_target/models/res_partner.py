# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models,fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_invoice_target = fields.Boolean()
