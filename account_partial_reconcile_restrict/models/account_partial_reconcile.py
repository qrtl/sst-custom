# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import ValidationError


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    def unlink(self):
        if not self.env.user.has_group("account.group_account_manager"):
            raise ValidationError(
                _(
                    "You need to be an accounting manager to be able to unreconcile records."
                )
            )
        return super(AccountPartialReconcile, self).unlink()
