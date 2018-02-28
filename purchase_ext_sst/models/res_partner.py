# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    update_lock = fields.Boolean(
        'Update Lock',
        help="If selected, the partner will not be updated through purchase "
             "order creation/update.",
    )
