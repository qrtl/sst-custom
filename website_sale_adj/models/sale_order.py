# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.osv import expression


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Store the earilest website_order_line's creation date
    order_line_date = fields.Datetime(
        'Order Date',
        compute='_get_order_line_date',
        store=True,
    )

    @api.multi
    @api.depends('order_line')
    def _get_order_line_date(self):
        for order in self:
            website_order_line = order.website_order_line
            order.order_line_date = website_order_line[0].create_date if website_order_line else False

    # Since quotation will be created after checked, use order_line_date to 
    # compute is_abandoned_cart field instead of date_order
    @api.multi
    @api.depends('team_id.team_type', 'order_line_date', 'order_line', 'state', 'partner_id')
    def _compute_abandoned_cart(self):
        abandoned_delay = float(self.env['ir.config_parameter'].sudo(
        ).get_param('website_sale.cart_abandoned_delay', '1.0'))
        abandoned_datetime = fields.Datetime.to_string(
            datetime.utcnow() - relativedelta(hours=abandoned_delay))
        for order in self:
            domain = order.order_line_date and order.order_line_date <= abandoned_datetime and order.team_id.team_type == 'website' and order.state == 'draft' and order.partner_id.id != self.env.ref(
                'base.public_partner').id and order.order_line
            order.is_abandoned_cart = bool(domain)

    def _search_abandoned_cart(self, operator, value):
        abandoned_delay = float(self.env['ir.config_parameter'].sudo(
        ).get_param('website_sale.cart_abandoned_delay', '1.0'))
        abandoned_datetime = fields.Datetime.to_string(
            datetime.utcnow() - relativedelta(hours=abandoned_delay))
        abandoned_domain = expression.normalize_domain([
            ('order_line_date', '<=', abandoned_datetime),
            ('team_id.team_type', '=', 'website'),
            ('state', '=', 'draft'),
            ('partner_id', '!=', self.env.ref('base.public_partner').id),
            ('order_line', '!=', False)
        ])
        # is_abandoned domain possibilities
        if (operator not in expression.NEGATIVE_TERM_OPERATORS and value) or (operator in expression.NEGATIVE_TERM_OPERATORS and not value):
            return abandoned_domain
        return expression.distribute_not(abandoned_domain)  # negative domain