# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
            filtered(lambda categ: request.env.user.partner_id.id in categ.message_partner_ids.ids).ids
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

    @http.route('/my/product_subscribes', type='http', auth="user",
                methods=['POST'], website=True)
    def product_subscribes(self, **kw):
        partner = request.env.user.partner_id

        public_categ_obj = request.env['product.public.category'].sudo()
        category_list = request.httprequest.form.getlist('categ_subscribe')

        category_list = [int(i) for i in category_list]
        selected_category_list = public_categ_obj.browse(category_list)
        subscribe_count = 0
        for subscribe_category in selected_category_list:
            if not subscribe_category.child_id:
                subscribe_count += subscribe_category.subscribe_point
        if partner.member_group_id and partner.member_group_id.point_limit < \
                subscribe_count:
            return self.portal_product_subscriptions(
                error=_('You subscription point is not enough to subscribe '
                        'the selected categories.'))
        subscribe_category_ids = selected_category_list.filtered(
            lambda i: partner.id not in i.message_partner_ids.ids
        )
        subscribe_categories = public_categ_obj.browse()
        if subscribe_category_ids:
            subscribe_categories = subscribe_category_ids.\
                _add_category_follower(partner)

        domain = [
            ('id', 'not in', subscribe_categories.ids + category_list),
        ]
        unsubscribe_category_ids = public_categ_obj.search(domain)
        unsubscribe_category_ids = unsubscribe_category_ids.filtered(
            lambda i: partner.id in i.message_partner_ids.ids
        )

        unsubscribe_categories = public_categ_obj.browse()
        if unsubscribe_category_ids:
            unsubscribe_categories = unsubscribe_category_ids.\
                _remove_category_follower(partner)

        vals = {
            'unsubscribe_category_ids': unsubscribe_categories,
            'subscribe_category_ids': subscribe_categories
        }
        return request.render(
            "website_sale_product_subscribe_notify.template_thanks_message",
            vals
        )
