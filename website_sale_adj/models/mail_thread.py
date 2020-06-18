# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import threading
from odoo import api, models, sql_db


class MailComposeMessage((models.TransientModel)):
    _inherit = 'mail.compose.message'

    # Added thread method.
    def mail_delay(self, composer=None, auto_commit=False):
        new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
        uid, context = self.env.uid, self.env.context
        with api.Environment.manage():
            self.env = api.Environment(new_cr, uid, context)
            if composer:
                composer.with_context(update_from_so=False).send_mail(
                    auto_commit=auto_commit)
        new_cr.commit()

    @api.multi
    def send_mail(self, auto_commit=False):
        if self._context.get('update_from_so'):
            timer = threading.Timer(
                30.0, self.mail_delay, args=(self, auto_commit))
            timer.start()
            return True
        return super(MailComposeMessage, self).send_mail(
            auto_commit=auto_commit)
