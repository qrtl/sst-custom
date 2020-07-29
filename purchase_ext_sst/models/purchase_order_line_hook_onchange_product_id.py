# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import SUPERUSER_ID, api, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from odoo.addons.purchase.models.purchase import PurchaseOrderLine


# Monkey Patching
# Overwrite the original onchange_product_id
# i.e. https://github.com/odoo/odoo/blob/11.0/addons/purchase/models/purchase.py#L781-L811 # noqa
@api.onchange("product_id")
def onchange_product_id(self):
    result = {}
    if not self.product_id:
        return result

    # Reset date, price and quantity since
    # _onchange_quantity will provide default values
    self.date_planned = (
        datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if not self.order_id.date_planned
        else self.order_id.date_planned
    )
    # Modified by QTL >>>
    # self.price_unit = self.product_qty = 0.0
    self.product_qty = 0.0
    # Modified by QTL <<<
    self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
    result["domain"] = {
        "product_uom": [("category_id", "=", self.product_id.uom_id.category_id.id)]
    }

    product_lang = self.product_id.with_context(
        lang=self.partner_id.lang, partner_id=self.partner_id.id,
    )
    self.name = product_lang.display_name
    if product_lang.description_purchase:
        self.name += "\n" + product_lang.description_purchase

    fpos = self.order_id.fiscal_position_id
    if self.env.uid == SUPERUSER_ID:
        company_id = self.env.user.company_id.id
        self.taxes_id = fpos.map_tax(
            self.product_id.supplier_taxes_id.filtered(
                lambda r: r.company_id.id == company_id
            )
        )
    else:
        self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id)

    self._suggest_quantity()
    self._onchange_quantity()

    return result


class PurchaseOrderLineHookOnchangeProductId(models.AbstractModel):
    _name = "purchase.order.line.hook.onchange.product.id"
    _description = "Provide hook point for onchange_product_id method"

    def _register_hook(self):
        PurchaseOrderLine.onchange_product_id = onchange_product_id
        return super(PurchaseOrderLineHookOnchangeProductId, self)._register_hook()
