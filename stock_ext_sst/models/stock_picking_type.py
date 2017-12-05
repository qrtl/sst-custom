# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    def _get_action(self, action_xmlid):
        action = super(StockPickingType, self)._get_action(action_xmlid)
        hide_carrier = 'False'
        if self and self.code != 'outgoing':
            hide_carrier = 'True'
        action['context'] = action['context'].replace('}', '''
                    'hide_carrier': %s,
}
        ''' % hide_carrier)
        return action
