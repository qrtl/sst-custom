# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from .hr_employee import REST_TIME


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    rest_time = fields.Selection(REST_TIME, "Rest Time (minutes)", default="0")
    classification = fields.Selection(
        [("work", "Work"), ("paid_leave", "Paid leave")],
        "Classification",
        default="work",
    )
    update_manually = fields.Boolean(string="Manual Update", default=False)
    update_manually_reason = fields.Text(string="Reason for Update",)
    working_hours = fields.Float("Working hours")
    work_location = fields.Char("Work Location")

    @api.onchange(
        "employee_id",
        "rest_time",
        "check_in",
        "check_out",
        "classification",
        "work_location",
    )
    def onchange_to_require_update_manually_reason(self):
        update_manually = False
        if type(self._origin.id) == type(1):
            update_manually = True
        self.update_manually = update_manually

    @api.onchange("employee_id")
    def onchange_employee(self):
        rest_time = "0"
        work_location = ""
        if self.employee_id and self.employee_id.rest_time_standard:
            rest_time = self.employee_id.rest_time_standard
        if self.employee_id and self.employee_id.work_location:
            work_location = self.employee_id.work_location

        self.rest_time = rest_time
        self.work_location = work_location

    @api.onchange("rest_time", "check_in", "check_out")
    def _compute_working_hours(self):
        worked_hours = 0
        if self.check_out and self.check_in:
            delta = datetime.strptime(
                self.check_out, DEFAULT_SERVER_DATETIME_FORMAT
            ) - datetime.strptime(self.check_in, DEFAULT_SERVER_DATETIME_FORMAT)
            worked_hours = delta.total_seconds() / 3600.0
            if self.rest_time:
                worked_hours -= float(self.rest_time) / 60.0
        self.working_hours = worked_hours

    @api.model
    def create(self, vals):
        res = super(HrAttendance, self).create(vals)
        res._compute_working_hours()
        return res

    @api.multi
    def write(self, vals):
        res = super(HrAttendance, self).write(vals)
        if (
            "rest_time" in vals.keys()
            or "check_in" in vals.keys()
            or "check_out" in vals.keys()
        ):
            for attendance in self:
                attendance._compute_working_hours()
        return res
