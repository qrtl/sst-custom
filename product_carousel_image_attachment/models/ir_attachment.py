# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

IMAGE_TYPES = ["image/png", "image/jpeg", "image/bmp", "image/gif"]


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model_create_multi
    def create(self, vals_list):
        attachments = super(IrAttachment, self).create(vals_list)
        for attachment in attachments:
            if attachment.mimetype in IMAGE_TYPES and attachment.res_model in [
                "product.template",
                "product.product",
            ]:
                vals = {}
                # assignment for pt and p
                if attachment.res_model == "product.template":
                    pt = self.env["product.template"].browse(attachment.res_id)
                    vals = {
                        "name": attachment.name,
                        "image_1920": attachment.datas,
                        "product_tmpl_id": pt.id,
                    }
                if attachment.res_model == "product.product":
                    p = self.env["product.product"].browse(attachment.res_id)
                    vals = {
                        "name": attachment.name,
                        "image_1920": attachment.datas,
                        "product_variant_id": p.id,
                    }
                self.env["product.image"].sudo().create(vals)
        return attachments
