# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models, api


_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _publish_product_custom(self, custom_domain, custom_fields):
        if custom_domain:
            domain = [('website_published', '=', False)]
            fields = {
                'website_published': True
            }
            try:
                domain += custom_domain or []
                fields.update(custom_fields or {})
                quants = self.search(domain)
                quants.update(fields)
                updated_products = len(quants.mapped(
                    'product_id').mapped('product_tmpl_id')) if quants else 0
                _logger.info(
                    '_publish_product_custom() is excuted and %s product records are updated. (custom_domain: %s, custom_fields: %s)',
                    updated_products, custom_domain, custom_fields)
            except Exception as e:
                _logger.error(
                    'Fail to excute _publish_product_custom() with custom_domain: %s and custom_fields %s, Traceback: %s',
                    custom_domain, custom_fields, e)
