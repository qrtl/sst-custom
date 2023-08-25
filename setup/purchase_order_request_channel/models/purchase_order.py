# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    request_channel_id = fields.Many2one("request.channel", "Request Channel")
