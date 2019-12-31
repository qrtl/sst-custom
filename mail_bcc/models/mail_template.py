# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class MailTemplate(models.Model):
    _inherit = "mail.template"

    email_bcc = fields.Char(
        'Bcc',
        help="Blind carbon copy recipients (placeholders may be used here)"
    )

    @api.multi
    def generate_recipients(self, results, res_ids):
        self.ensure_one()
        res = super(MailTemplate, self).generate_recipients(results, res_ids)
        email_bcc = self.env.context.get('email_bcc')
        if email_bcc:
            for res_id, values in res.items():
                res[res_id]['email_bcc'] = email_bcc
        return res
