# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QuantSaleOrderWizard(models.TransientModel):
    _name = 'quant.sale.order.wizard'

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
    )
    team_id = fields.Many2one(
        'crm.team',
        string='Sales Channel',
        required=True,
    )

    @api.model
    def default_get(self, fields):
        """Raise to warning in
            - selected quants not in same location.
            - selected quants are already create sale order.
            - selected quants company is not same to user company.
        """
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        active_model = context.get('active_model')
        quant_ids = self.env[active_model].browse(active_ids)
        source_location = quant_ids[0].location_id
        if any(q.location_id != source_location for q in quant_ids):
            raise UserError(_('Please select quants that are in the same '
                              'Location.'))
        if source_location.usage != 'internal':
            raise UserError(_('Please select quants that are in the internal '
                              'location to create the sales order.'))
        order_line_list = self.env['sale.order.line'].search([
            ('state', 'not in', ['done', 'cancel']),
            ('product_id', 'in', [q.product_id.id for q in quant_ids])
        ])
        if order_line_list:
            error_msg = ''
            for order_line in order_line_list:
                error_msg += '\n%s: %s' % (
                    order_line.order_id.name,
                    order_line.product_id.display_name,
                )
            raise UserError(_('There is at least one active sales order '
                              'that uses the product of a selected quant: '
                              '%s') % error_msg)
        if any(self .env.user.company_id.id != q.company_id.id for q in
               quant_ids):
            raise UserError(_('You cannot create sales order from stock '
                              'quants that belongs to other company.'))
        return super(QuantSaleOrderWizard, self).default_get(fields)

    @api.multi
    def action_create_sale_order(self):
        '''This method create a sale order.'''
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        stock_quant_obj = self.env['stock.quant']
        quant_ids = stock_quant_obj.browse(active_ids)
        warehouse_id = self.get_warehouse_id(quant_ids[0].location_id)
        sale_order_obj = self.env['sale.order']
        order_vals = {
            'partner_id': self.partner_id.id,
            'team_id': self.team_id.id,
            'company_id': self.env.user.company_id.id,
            'state': 'draft',
            'warehouse_id': warehouse_id.id,
        }
        sale_order = sale_order_obj.sudo().create(order_vals)
        sale_order.onchange_partner_id()
        sale_order.team_id = self.team_id.id
        sale_order.user_id = self.env.uid

        # A list to store the values of sale.order.line's required fieds
        order_lines_value_list = []
        # A dict to store the tax_id of each product
        product_tax_id = {}
        for quant in quant_ids:
            product = quant.product_id
            # Calculate the tax_id and price_unit of the order line
            if product.id not in product_tax_id:
                tax_id = self.get_tax_id(sale_order, product)
                product_tax_id[product.id] = tax_id
            price_unit = self.env[
                'account.tax']._fix_tax_included_price_company(
                self.get_display_price(sale_order, product, quant.quantity),
                product.taxes_id, product_tax_id[product.id], sale_order.company_id) if \
                sale_order.pricelist_id else product.list_price
            # get order line description
            name = product.name_get()[0][1]
            if product.description_sale:
                name += '\n' + product.description_sale
            # get purchase_price
            purchase_price = self.env['sale.order.line']._get_purchase_price(
                sale_order.pricelist_id,
                product,
                product.uom_id,
                fields.Date.context_today(self)
            )['purchase_price']
            # Add all the required values to the list
            order_lines_value_list.append(
                "('%s', %s, %s, %s, %s, %s, %s, %s, %s, 0, 0, %s, 0, 'f', "
                "'f', %s, (now() at time zone 'UTC'))" % (
                    name,
                    product.id,
                    int(quant.quantity),
                    product.uom_id.id,
                    sale_order.id,
                    int(price_unit),
                    int(price_unit),
                    int(purchase_price),
                    product.product_tmpl_id.sale_delay,
                    int(quant.quantity),
                    self.env.user.id
                )
            )
        order_lines_values = ','.join(order_lines_value_list)
        # Use Insert SQL to improve the performance, create() takes much longer time on
        # multiple records creation.
        self.env.cr.execute("""
            INSERT INTO sale_order_line (
                name,
                product_id,
                product_uom_qty,
                product_uom,
                order_id,
                price_unit,
                price_reduce,
                purchase_price,
                customer_lead,
                discount,
                qty_delivered,
                qty_to_deliver,
                qty_invoiced,
                is_downpayment,
                is_delivery,
                create_uid,
                create_date
            )
            VALUES %s
        """ % order_lines_values)
        # Update the tax_id
        for order_line in sale_order.order_line:
            order_line.tax_id = product_tax_id[order_line.product_id.id]

        action = self.env.ref('sale.action_quotations')
        action_vals = action.read()[0]
        action_vals['domain'] = str([('id', '=', sale_order.id)])
        return action_vals

    def get_warehouse_id(self, location_id):
        stock_warehouse_obj = self.env['stock.warehouse']

        location_list = []
        location = location_id
        while location:
            location_list.append(location.id)
            location = location.location_id

        warehouse_id = stock_warehouse_obj.search(
            [('view_location_id', 'in', location_list),
             ('company_id', '=', self.env.user.company_id.id)],
            limit=1
        )
        if not warehouse_id:
            raise UserError(_('The stock location does not belong to any '
                              'warehouse.'))
        return warehouse_id

    # Same logic as sale.order.line's _compute_tax_id(), but the method will
    # return the account.tax record(s)
    # https://github.com/odoo/odoo/blob/11.0/addons/sale/models/sale.py#L836-L842
    def get_tax_id(self, sale_order, product):
        fpos = sale_order.fiscal_position_id or \
               sale_order.partner_id.property_account_position_id
        taxes = product.taxes_id.filtered(
            lambda r: not sale_order.company_id or r.company_id ==
                      sale_order.company_id)
        return fpos.map_tax(taxes, product,
                            sale_order.partner_shipping_id) if fpos else taxes

    # Same logic as sale.order.line's get_display_price()
    # https://github.com/odoo/odoo/blob/11.0/addons/sale/models/sale.py#L1036-L1047
    def get_display_price(self, sale_order, product, product_uom_qty):
        if sale_order.pricelist_id.discount_policy == 'with_discount':
            return product.with_context(
                pricelist=sale_order.pricelist_id.id).price
        product_context = dict(self.env.context,
                               partner_id=sale_order.partner_id.id,
                               date=sale_order.date_order,
                               uom=product.uom_id.id)
        final_price, rule_id = sale_order.pricelist_id.with_context(
            product_context).get_product_price_rule(product,
                                                    product_uom_qty or
                                                    1.0, sale_order.partner_id)
        base_price, currency_id = self.with_context(
            product_context)._get_real_price_currency(product, rule_id,
                                                      product_uom_qty,
                                                      product.product_uom,
                                                      sale_order.pricelist_id.id)
        if currency_id != sale_order.pricelist_id.currency_id.id:
            base_price = self.env['res.currency'].browse(
                currency_id).with_context(product_context).compute(
                base_price, sale_order.pricelist_id.currency_id)
        return max(base_price, final_price)
