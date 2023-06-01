# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Irattachemnt(models.Model):
    _inherit = "ir.attachment"

    is_done = fields.Boolean()

    def _image_job_queue(self):
        mapping = {
            "product.template": "image",
            "product.image": "image",
            "product.public.category": "image",
            "res.partner": "image",
            "res.users": "image",
        }
        for model, field in mapping.items():
            attachments = self.search(
                [
                    ("res_model", "=", model),
                    ("res_field", "=", field),
                    ("res_id", "!=", False),
                    ("is_done", "=", False),
                ]
            )
            for attachment in attachments:
                self.with_delay()._convert_image_attachments(model, attachment)
                attachment.is_done = True

    def _convert_image_attachments(self, model, attachment):
        self.env[model].browse(attachment.res_id).image_1920 = attachment.datas
