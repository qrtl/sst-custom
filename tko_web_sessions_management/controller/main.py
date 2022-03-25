# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import simplejson
from odoo import http
from odoo.http import request


class websession(http.Controller):
    @http.route(['/ajax/session/'], auth="public", website=True)
    def property_map(self, **kwargs):
        context = {}
        sessions = request.env['ir.sessions'].sudo().search([
            ('logged_in', '=', True),
            ('user_id', '=', request.session.uid)])
        if sessions:
            return simplejson.dumps(context)
        context = {'Content-Type': 'application/json;charset=utf-8',
                   'result': 'true'}
        if request.session:
            request.session.logout(keep_db=True)
        return simplejson.dumps(context)
