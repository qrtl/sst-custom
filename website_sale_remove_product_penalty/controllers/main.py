# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart/update_json'], type='json', auth="public",
                methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None,
                         set_qty=None, display=True):
        if line_id and set_qty != None and not add_qty:
            sale_order_line = request.env['sale.order.line'].sudo().browse(
                line_id)
            penalty_product_id = request.env[
                'ir.config_parameter'].sudo().get_param(
                'website_sale_remove_product_penalty.penalty_product_id')
            # Since this method will only be called on frontend, no need to
            # check whether it is a "Website Sales" order or not.
            if sale_order_line.product_uom_qty > set_qty and \
                    penalty_product_id and sale_order_line.product_id.type \
                    == 'product':
                penalty_product = request.env['product.product'].sudo().browse([
                    int(penalty_product_id)])[0]
                # Get the quantity removed from the cart
                quantity = sale_order_line.product_uom_qty - set_qty
                sale_order = sale_order_line.order_id
                penalty_flag = False
                for order_line in sale_order.order_line:
                    # Check the sales order and see if there is already a
                    # penalty product order line
                    if order_line.product_id == penalty_product:
                        order_line.product_uom_qty += quantity
                        penalty_flag = True
                    # Add a new penalty order line
                if not penalty_flag:
                    sale_order._create_order_line(penalty_product, quantity)
                # Record the deletion to the removal history
                sale_order.sudo().write({
                    'cart_product_removal_history_ids': [(0, 0, {
                        'product_id': sale_order_line.product_id.id,
                        'reason': _('Removed by user'),
                        'is_read': True,
                    })]
                })
        return super(WebsiteSale, self).cart_update_json(
            product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty,
            display=display)
