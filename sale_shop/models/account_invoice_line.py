# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.sale_line_ids and res.sale_line_ids[0].order_id.warehouse_id:
            res.invoice_id.shop_id = res.sale_line_ids[0].order_id.warehouse_id.id
        return res
