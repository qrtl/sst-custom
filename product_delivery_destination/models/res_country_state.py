# Copyright 2023 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    is_deliverable = fields.Boolean()
