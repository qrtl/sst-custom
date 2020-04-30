# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import threading
from odoo import api, models, sql_db


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    # Added thread method.
    def mail_delay(self, composer=None):
        new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
        uid, context = self.env.uid, self.env.context
        with api.Environment.manage():
            self.env = api.Environment(new_cr, uid, context)
            if composer:
                composer = self.env['mail.compose.message'].browse(
                    composer.id)
                composer.send_mail()
        new_cr.commit()

    # Overwrite message_post_with_template and added thread to send email
    # delay.
    @api.multi
    def message_post_with_template(self, template_id, **kwargs):
        """ Helper method to send a mail with a template
            :param template_id : the id of the template to render
             to create the body of the message
            :param **kwargs : parameter to create a mail.compose.message
             woaerd (which inherit from mail.message)
        """
        # Get composition mode, or force it according
        # to the number of record in self
        if not kwargs.get('composition_mode'):
            kwargs['composition_mode'] = 'comment' if len(
                self.ids) == 1 else 'mass_mail'
        if not kwargs.get('message_type'):
            kwargs['message_type'] = 'notification'
        res_id = kwargs.get('res_id', self.ids and self.ids[0] or 0)
        res_ids = kwargs.get('res_id') and [kwargs['res_id']] or self.ids

        # Create the composer
        composer = self.env['mail.compose.message'].with_context(
            active_id=res_id,
            active_ids=res_ids,
            active_model=kwargs.get('model', self._name),
            default_composition_mode=kwargs['composition_mode'],
            default_model=kwargs.get('model', self._name),
            default_res_id=res_id,
            default_template_id=template_id,
        ).create(kwargs)
        # Simulate the onchange (like trigger in form the view) only
        # when having a template in single-email mode

        if template_id:
            update_values = composer.onchange_template_id(
                template_id, kwargs['composition_mode'],
                self._name, res_id)['value']
            composer.write(update_values)
        if self._context.get('update_from_so'):
            timer = threading.Timer(
                30.0, self.mail_delay, args=(composer))
            timer.start()
            return True
        return composer.send_mail()
