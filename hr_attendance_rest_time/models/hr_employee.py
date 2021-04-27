# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import exceptions, fields, models

REST_TIME = [
    ("0", "0"),
    ("15", "15"),
    ("30", "30"),
    ("45", "45"),
    ("60", "60"),
    ("75", "75"),
    ("90", "90"),
]


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    rest_time_standard = fields.Selection(
        REST_TIME, "Standard Rest Time (minutes)", default="0"
    )

    def attendance_action_change(self):
        if len(self) > 1:
            raise exceptions.UserError(
                _(
                    """Cannot perform check in or check out on multiple employees
                ."""
                )
            )
        auto_rest_time_standard = False
        if self.attendance_state == "checked_in":
            auto_rest_time_standard = True
        attendance = super(HrEmployee, self).attendance_action_change()
        update_vals = {}
        if auto_rest_time_standard:
            if self.rest_time_standard and not attendance.rest_time:
                update_vals.update({"rest_time": self.rest_time_standard})
            if self.work_location and not attendance.work_location:
                update_vals.update({"work_location": self.work_location})
        attendance.write(update_vals)
        return attendance
