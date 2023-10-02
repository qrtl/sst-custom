# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockQuantProductPublish(models.TransientModel):
    _name = "stock.quant.product.publish.wizard"

    yahoo_product_state_id = fields.Many2one(
        "yahoo.product.state", string="Yahoo Product State",
    )

    def action_stock_quant_publish(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", [])
        quants = self.env["stock.quant"].browse(active_ids)
        values = {
            "website_published": True,
            "yahoo_product_state_id": self.yahoo_product_state_id.id,
        }
        # Using mapped to gather all product_tmpl_id records
        product_templates = quants.mapped('product_id.product_tmpl_id')
        product_templates.sudo().write(values)
