# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Irattachemnt(models.Model):
    _inherit = "ir.attachment"

    binary_conversion_queued = fields.Boolean()

    def _binary_conversion_job_queue(self, limit=1000):
        attachments = self.env["ir.attachment"].search(
            [
                ("db_datas", "!=", False),
                ("binary_conversion_queued", "=", False),
            ],
            limit=limit,
        )
        for attachment in attachments:
            desc = "Attachment:" + str(attachment.res_id)
            self.with_delay(description=desc)._convert_db_stored_attachments(attachment)
            attachment.binary_conversion_queued = True

    def _convert_db_stored_attachments(self, attachment):
        # Decoding base64 encoded data to binary
        binary_data = base64.b64decode(attachment.db_datas)
        attachment.write({"db_datas": binary_data})
