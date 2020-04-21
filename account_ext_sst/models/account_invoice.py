# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    shop_id = fields.Many2one(
        "stock.warehouse",
        string="Shop",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.onchange("invoice_line_ids")
    def invoice_line_ids_onchange(self):
        if self.invoice_line_ids and not self.shop_id:
            for invoice_line_id in self.invoice_line_ids:
                if invoice_line_id.purchase_id and invoice_line_id.purchase_id.shop_id:
                    self.shop_id = invoice_line_id.purchase_id.shop_id.id
                    return

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        res.invoice_line_ids_onchange()
        return res
