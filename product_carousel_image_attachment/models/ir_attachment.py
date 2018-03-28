# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import image_resize_image

IMAGE_TYPES = ['image/png', 'image/jpeg', 'image/bmp', 'image/gif']


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def create(self, vals):
        #here we resize the image first to avoid bloating the filestore
        if vals.get('res_model') in ['product.template', 'product.product']:
            mimetype = vals.get('mimitype') or self._compute_mimetype(vals)
            if mimetype in IMAGE_TYPES:
                vals['datas'] = image_resize_image(vals['datas'],
                                                   size=(1600, 1600),
                                                   encoding='base64',
                                                   filetype=None,
                                                   avoid_if_small=True)
        attachment = super(IrAttachment, self).create(vals)
        if attachment and attachment.mimetype in IMAGE_TYPES and \
                        attachment.res_model in ['product.template',
                                                 'product.product']:
            #FIXME in case variants are used, how should we normalize the value
            #assignment for pt and pp below?
            if attachment.res_model == 'product.template':
                pt = self.env['product.template'].browse(attachment.res_id)
                pp = pt.product_variant_id
            if attachment.res_model == 'product.product':
                pp = self.env['product.product'].browse(attachment.res_id)
                pt = pp.product_tmpl_id
            vals = {
                'name': attachment.name,
                'image': attachment.datas,
                'image_url': attachment.local_url,
                'product_tmpl_id': pt.id,
                'product_variant_id': pp.id,
            }
            self.env['product.image'].sudo().create(vals)
        return attachment
