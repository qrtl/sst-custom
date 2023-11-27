# Copyright 2023 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    restrict_edit = fields.Boolean(
        help="Enable to restrict the editing record for non-system users."
    )

    def write(self, values):
        if self.env.user.has_group("base.group_system"):
            return super(ResPartner, self).write(values)
        if self.env.is_superuser():
            return super(ResPartner, self).write(values)
        for record in self:
            if record.restrict_edit:
                raise UserError(_("You are not allowed to modify this partner record."))
        return super(ResPartner, self).write(values)
