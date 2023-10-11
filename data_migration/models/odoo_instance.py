# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OdooInstance(models.Model):
    _name = "odoo.instance"
    _description = "Odoo Instances"

    name = fields.Char(required=True)
    instance_url = fields.Char(required=True)
    instance_db = fields.Char(required=True)
    login = fields.Char(required=True)
    password = fields.Char(required=True)
