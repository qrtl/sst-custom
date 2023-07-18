# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    is_deliverable = fields.Boolean()
