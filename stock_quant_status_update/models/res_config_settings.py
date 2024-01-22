# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    picking_product_state_id = fields.Many2one(
        "yahoo.product.state", string="State For Finished Picking Product"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env["ir.config_parameter"].sudo().get_param
        res.update(
            picking_product_state_id=int(
                get_param("stock_quant_status_update.picking_product_state_id", default=False)
            )
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env["ir.config_parameter"].sudo().set_param
        set_param(
            "stock_quant_status_update.picking_product_state_id", self.picking_product_state_id.id
        )
