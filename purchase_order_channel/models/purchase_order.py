# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    call_back = fields.Boolean("Call Back")
    request_channel_id = fields.Many2one("request.channel", "Request Channel")
    request_medium_id = fields.Many2one("request.medium", "Request Medium")
