# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    restrict_edit = fields.Boolean(
        help="Enable to restrict the editing record for non-system users."
    )

    def write(self, values):
        if (
            self.env.user.has_group("partner_edit_restrict.group_partner_edit")
            or self.env.user._is_superuser()
        ):
            return super().write(values)
        restricted_recs = self.filtered(lambda x: x.restrict_edit)
        if restricted_recs:
            names = ", ".join(restricted_recs.mapped("name"))
            raise UserError(
                _("You are not allowed to modify following partner: %s")
                %(names)
            )
        return super().write(values)
