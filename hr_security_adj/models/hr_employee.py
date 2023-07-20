# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    # barcode field is used in field's attribute. So, we need to add operator group
    # to this field for not getting error when we open employee form view.
    barcode = fields.Char(groups="hr.group_hr_user,hr_security_adj.group_hr_operator")
