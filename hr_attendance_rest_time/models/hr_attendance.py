# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from .hr_employee import REST_TIME


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    rest_time = fields.Selection(REST_TIME, "Rest Time (minutes)")
    attendance_categ = fields.Selection(
        [("work", "Work"), ("paid_leave", "Paid Leave")], "Category", default="work",
    )
    manual_update = fields.Boolean("Manual Update")
    manual_update_reason = fields.Selection(
        [("forgot", "Forgot to check-in/check-out"), ("other", "Other")],
        string="Manual Update Reason",
    )
    manual_update_reason_desc = fields.Char("Manual Update Reason Description")
    work_location = fields.Char("Work Location")

    @api.onchange("employee_id", "check_in", "check_out")
    def _onchange_manual_update(self):
        self.manual_update = True

    @api.onchange("employee_id")
    def onchange_employee(self):
        employee = self.employee_id
        self.rest_time = employee.rest_time_standard if employee else False
        self.work_location = employee.work_location if employee else False

    @api.depends("check_in", "check_out", "rest_time")
    def _compute_worked_hours(self):
        super()._compute_worked_hours()
        for attendance in self:
            if attendance.worked_hours and attendance.rest_time:
                rest_time = float(attendance.rest_time) / 60.0
                if attendance.worked_hours > rest_time:
                    attendance.worked_hours -= rest_time
                else:
                    attendance.worked_hours = 0.0
