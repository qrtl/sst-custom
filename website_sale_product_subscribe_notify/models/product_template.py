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
                    limit_recipient = rec.env['ir.default'].get('res.config.settings', 'email_recipient_limit')
                    number_of_loop = round(len(partners)/limit_recipient)

                    ctx.update({
                            'website_published_update': vals.get(
                                "website_published"),
                            'list_price_update': vals.get("list_price"),
                            'description_sale_update': vals.get("description_sale"),
                            'partner_ids': ','.join([str(partner.id) for partner in partners[:limit_recipient]]),
                            'list_price': list_price
                    })
                    template.with_context(ctx).send_mail(rec.id)
        return result

    def get_website_name(self):
        return self.env['website'].get_current_website().name

    def get_product_category_followers_ids(self):
        partner_ids = []
        for category in self.public_categ_ids:
            partner_ids += list(
                set(category.message_partner_ids.ids) -
                set(partner_ids)
            )
        return partner_ids
