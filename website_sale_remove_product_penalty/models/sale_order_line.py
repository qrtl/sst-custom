# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_penalty = fields.Boolean(string="Is a Penalty", default=False)

    @api.multi
    def unlink(self):
        penalty_product_id = self.env['ir.config_parameter'].sudo().get_param(
            'website_sale_remove_product_penalty.penalty_product_id')
        if penalty_product_id:
            penalty_product = self.env['product.product'].browse([
                int(penalty_product_id)])[0]
            for order_line in self:
                if order_line.order_id and order_line.team_id == self.env.ref(
                        'sales_team.salesteam_website_sales') and \
                                order_line.product_id.type == 'product':
                    # Check the sales order and see if there is already a
                    # penalty product order line
                    penalty_flag = False
                    for sale_order_line in order_line.order_id.order_line:
                        if sale_order_line.product_id == penalty_product:
                            sale_order_line.product_uom_qty += 1
                            penalty_flag = True
                    # Add a new penalty order line
                    if not penalty_flag:
                        order_line.order_id._create_order_line(penalty_product)
        res = super(SaleOrderLine, self).unlink()
        return res
