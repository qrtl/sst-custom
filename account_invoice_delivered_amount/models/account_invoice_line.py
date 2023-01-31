# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    is_delivered = fields.Boolean(string="Deliverd", compute="_compute_delivered_amount", store=True)
    deliverd_amount = fields.Monetary(string='Delivered Amount',
        store=True, compute='_compute_delivered_amount')
    
    @api.depends("sale_line_ids", "product_id", "quantity")
    def _compute_delivered_amount(self):
        for line in self:
            if line.sale_line_ids:
                if line.product_id.type == "service":
                    line.is_delivered = True
                    line.deliverd_amount = line.quantity * line.price_unit
                else:
                    qty_delivered = sum([x.qty_delivered for x in line.sale_line_ids])
                    if qty_delivered > 0:
                        line.is_delivered = True
                        line.deliverd_amount = qty_delivered * line.price_unit
                        break
                    line.is_delivered = False
                    line.deliverd_amount = 0
            else:
                line.is_delivered = False
                line.deliverd_amount = 0
