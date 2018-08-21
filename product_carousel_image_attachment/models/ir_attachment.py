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
        mimetype = vals.get('mimitype') or self._compute_mimetype(vals)
        if mimetype in IMAGE_TYPES and 'datas' in vals:
            # image_resize_image requires a binary object instead of string.
            # For situations like adding images to the product_image_ids
            # through Odoo's standard way, vals['datas'] will be in string
            # form therefore conversion is needed
            datas = vals['datas'].encode('utf8') if type(vals['datas']) is \
                                                    str else vals['datas']
            vals['datas'] = image_resize_image(datas,
                                               size=(1024, 1024),
                                               encoding='base64',
                                               filetype=None,
                                               avoid_if_small=True)
        attachment = super(IrAttachment, self).create(vals)
        #if datas_fname is False, then we judge it as the main image, and we
        #do not want to add carousel image for that
        if attachment and attachment.mimetype in IMAGE_TYPES and \
                        attachment.res_model in ['product.template',
                                                 'product.product'] and \
                        attachment.datas_fname:
            #assignment for pt
            if attachment.res_model == 'product.template':
                pt = self.env['product.template'].browse(attachment.res_id)
            if attachment.res_model == 'product.product':
                pt = self.env['product.product'].browse(
                    attachment.res_id).product_tmpl_id
            vals = {
                'name': attachment.name,
                'image': attachment.datas,
                'product_tmpl_id': pt.id,
            }
            self.env['product.image'].sudo().create(vals)
        return attachment
