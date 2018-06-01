# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        for rec in self:
            if rec.website_published:
                if vals.get("website_published") or vals.get("list_price") \
                        or vals.get('description_sale') and \
                                rec.description_sale:
                    ctx = self._context.copy()
                    template = self.env.ref(
                        'website_sale_product_subscribe_notify.email_template_product_public_category',
                        False
                    )
                    partner_ids = rec.get_product_category_followers_ids()
                    partners = rec.env['res.partner'].browse(partner_ids)
                    list_price = "%d" % int(rec.list_price)
                    for partner in partners:
                        ctx.update({
                            'partner_name': partner.name,
                            'partner_id': partner.id,
                            'list_price': list_price
                        })
                        template.with_context(ctx).send_mail(rec.id)
        return result

    def get_website_name(self):
        return self.env['website'].get_current_website().name

    def get_product_category_followers_ids(self):
        partner_ids = []
        for category in self.public_categ_ids:
            category_id = category
            while(category_id):
                partner_ids += list(
                    set(category_id.message_partner_ids.ids) -
                    set(partner_ids)
                )
                category_id = category_id.parent_id
        return partner_ids
