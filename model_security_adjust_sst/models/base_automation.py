# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BaseAutomation(models.Model):
    _inherit = "base.automation"

    def _process(self, records):
        """Process action ``self`` on
        the ``records`` that have not been done yet."""
        # filter out the records on which self has already been done
        action_done = self._context["__action_done"]
        records_done = action_done.get(self, records.browse())
        records -= records_done
        if not records:
            return

        # mark the remaining records as done (to avoid recursive processing)
        action_done = dict(action_done)
        action_done[self] = records_done + records
        self = self.with_context(__action_done=action_done)
        records = records.with_context(__action_done=action_done)

        # modify records
        values = {}
        if "date_action_last" in records._fields:
            values["date_action_last"] = fields.Datetime.now()
        if values:
            records.write(values)

        # execute server actions
        # QTL Edit: Access ir.actions.server with sudo()
        # if self.action_server_id:
        if self.sudo().action_server_id:
            for record in records:
                ctx = {
                    "active_model": record._name,
                    "active_ids": record.ids,
                    "active_id": record.id,
                }
                # self.action_server_id.with_context(**ctx).run()
                self.sudo().action_server_id.with_context(**ctx).run()
