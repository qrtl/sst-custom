# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def invoice_validate(self):
        result = super(AccountInvoice, self).invoice_validate()
        for account_invoice in self:
            if (
                account_invoice.state in ("open", "paid")
                and account_invoice.type == "out_invoice"
            ):
                for invoice_line in account_invoice.invoice_line_ids:
                    product = invoice_line.product_id.product_tmpl_id
                    product.write(
                        {
                            "sale_price_unit": invoice_line.price_total
                            / invoice_line.quantity,
                        }
                    )
        return result
