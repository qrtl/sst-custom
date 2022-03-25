# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

import werkzeug.contrib.sessions
import werkzeug.datastructures
import werkzeug.exceptions
import werkzeug.local
import werkzeug.routing
import werkzeug.wrappers
import werkzeug.wsgi
from odoo import SUPERUSER_ID, api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

LOGOUT_TYPES = [('ul', 'User Logout'),
                ('to', 'Session Timeout'),
                ('sk', 'Session Killed'), ]


class ir_sessions(models.Model):
    _name = 'ir.sessions'
    _description = "Sessions"

    user_id = fields.Many2one('res.users', 'User', ondelete='cascade',
                              required=True)
    logged_in = fields.Boolean('Logged in', required=True, index=True)
    session_id = fields.Char('Session ID', size=100, required=True)
    session_seconds = fields.Integer('Session duration in seconds')
    multiple_sessions_block = fields.Boolean('Block Multiple Sessions')
    date_login = fields.Datetime('Login', required=True)
    date_logout = fields.Datetime('Logout')
    date_expiration = fields.Datetime(
        'Expiration Date', required=True, index=True,
        default=lambda *a: fields.Datetime.now())
    logout_type = fields.Selection(LOGOUT_TYPES, 'Logout Type')
    session_duration = fields.Char('Session Duration')
    user_kill_id = fields.Many2one('res.users', 'Killed by', )
    unsuccessful_message = fields.Char('Unsuccessful', size=252)
    ip = fields.Char('Remote IP', size=15)
    ip_location = fields.Char('IP Location', )
    remote_tz = fields.Char('Remote Time Zone', size=32, required=True)
    # Add other fields about the sessions from HEADER...

    _order = 'logged_in desc, date_expiration desc'

    # scheduler function to validate users session
    @api.model
    def validate_sessions(self):
        sessions = self.sudo().search([
            ('date_expiration', '<=',
             fields.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
            ('logged_in', '=', True)])
        if sessions:
            sessions._close_session(logout_type='to')
        return True

    @api.multi
    def action_close_session(self):
        redirect = self._close_session(logout_type='sk')
        if redirect:
            return werkzeug.utils.redirect(
                '/web/login?db=%s' %
                self.env.cr.dbname, 303)

    @api.multi
    def _on_session_logout(self, logout_type=None):
        now = fields.datetime.now()
        cr = self.pool.cursor()
        # autocommit: our single update request will be performed atomically.
        # (In this way, there is no opportunity to have two transactions
        # interleaving their cr.execute()..cr.commit() calls and have one
        # of them rolled back due to a concurrent access.)
        cr.autocommit(True)

        for session in self:
            session_duration = str(now - datetime.strptime(
                session.date_login,
                DEFAULT_SERVER_DATETIME_FORMAT)).split('.')[0]
            session.sudo().write(
                {
                    'logged_in': False,
                    'date_logout':
                        now.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'logout_type': logout_type,
                    'user_kill_id': SUPERUSER_ID,
                    'session_duration': session_duration,
                })
        cr.commit()
        cr.close()
        return True

    @api.multi
    def _close_session(self, logout_type=None):
        redirect = False
        for r in self:
            if r.user_id.id == self.env.user.id:
                redirect = True
            r._on_session_logout(logout_type)
        return redirect
