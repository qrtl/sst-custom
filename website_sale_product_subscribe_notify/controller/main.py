# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        child_categories = request.env['product.public.category'].search([
            ('child_id', '=', False)
        ])
        subscribe_count = request.env['mail.followers'].search_count([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('res_model', '=', 'product.public.category'),
            ('res_id', 'in', child_categories.ids)
        ])
        values.update({
            'product_subscription_count': subscribe_count,
        })
        return values

    @http.route([
        '/my/product_subscriptions',
        '/my/product_subscriptions/page/<int:page>',
    ],
        type='http', auth="user", website=True)
    def portal_product_subscriptions(self, **kw):
        values = self._prepare_portal_layout_values()
        product_public_category = request.env['product.public.category']
        domain = []
        product_subscriptions = product_public_category.sudo().search(domain)
        parent_product_subscription = product_public_category.sudo().search([
            ('parent_id', '=', False)
        ])
        product_public_category_lst = product_public_category.search([]).\
            filtered(
                lambda categ: request.env.user.partner_id.id in categ.message_partner_ids.ids).ids
        if 'error' in kw:
            values.update({
                'error': kw.get('error'),
            })
        values.update({
            'product_subscriptions': product_subscriptions,
            'parent_product_subscription': parent_product_subscription,
            'product_public_category_lst': product_public_category_lst,
            'page_name': 'Product Subscriptions',
            'default_url': '/my/product_subscriptions',
        })
        return request.render(
            "website_sale_product_subscribe_notify.display_product_subscriptions",
            values
        )

    @http.route('/my/product_subscribes', type='http', auth="user", methods=['POST'], website=True)
    def product_subscribes(self, **kw):
        partner = request.env.user.partner_id
        # Retrieve the categories selection from the form
        category_list = [
            int(i) for i in request.httprequest.form.getlist('categ_subscribe')]
        selected_category_list = request.env['product.public.category'].sudo().browse(
            category_list)

        # Check total points needed for the categories and partner's point limit
        subscribe_point_count = 0
        for subscribe_category in selected_category_list:
            if not subscribe_category.child_id:
                subscribe_point_count += subscribe_category.subscribe_point
        if partner.member_group_id and partner.member_group_id.point_limit < \
                subscribe_point_count or not partner.member_group_id:
            return self.portal_product_subscriptions(
                error=_('You subscription point is not enough to subscribe '
                        'the selected categories.'))

        # Filter and subscribe the selected categories that are not yet subscribed
        subscribe_category_ids = selected_category_list.filtered(
            lambda i: partner.id not in i.message_partner_ids.ids
        )
        subscribe_category_ids.sudo().message_subscribe(
            partner_ids=[partner.id])

        # Check and unsubscribe unselected categories
        unsubscribe_category_ids = request.env['product.public.category'].sudo().search(
            [('id', 'not in', category_list)])
        unsubscribe_category_ids = unsubscribe_category_ids.filtered(
            lambda i: partner.id in i.message_partner_ids.ids
        )
        unsubscribe_category_ids.sudo().message_unsubscribe(
            partner_ids=[partner.id])

        # Return the subscriptions updates
        vals = {
            'unsubscribe_category_ids': unsubscribe_category_ids,
            'subscribe_category_ids': subscribe_category_ids,
        }
        return request.render(
            "website_sale_product_subscribe_notify.template_thanks_message",
            vals
        )
