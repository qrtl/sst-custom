# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _check_carrier_quotation(self, force_carrier_id=None):
        res = super(SaleOrder, self)._check_carrier_quotation(
            force_carrier_id=force_carrier_id
        )
        if self.carrier_id and self.carrier_id.delivery_warehouse_id:
            self.warehouse_id = self.carrier_id.delivery_warehouse_id
        return res
