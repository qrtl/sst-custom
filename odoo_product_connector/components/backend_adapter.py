# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import socket
import logging
import xmlrpc.client
import odoorpc

from odoo.addons.component.core import AbstractComponent
from odoo.addons.queue_job.exception import RetryableJobError
from odoo.addons.connector.exception import NetworkRetryableError
from datetime import datetime

_logger = logging.getLogger(__name__)

try:
    import magento as magentolib
except ImportError:
    _logger.debug("Cannot import 'magento'")


MAGENTO_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class OdooLocation(object):

    def __init__(self, location, username, password,
                 use_custom_api_path=False):
        self._location = location
        self.username = username
        self.password = password
        self.use_custom_api_path = use_custom_api_path

        self.use_auth_basic = False
        self.auth_basic_username = None
        self.auth_basic_password = None

    @property
    def location(self):
        location = self._location
        if not self.use_auth_basic:
            return location
        assert self.auth_basic_username and self.auth_basic_password
        replacement = "%s:%s@" % (self.auth_basic_username,
                                  self.auth_basic_password)
        location = location.replace('://', '://' + replacement)
        return location


class OdooAPI(object):

    def __init__(self, location):
        """
        :param location: Odoo location
        :type location: :class:`OdooLocation`
        """
        self._location = location
        # self._api = None
        self._odoo = odoorpc.ODOO(location.location, protocol='jsonrpc+ssl', port=443)

    # @property
    # def api(self):
    #     if self._api is None:
    #         # custom_url = self._location.use_custom_api_path
    #         odoo = odoorpc.ODOO(self._location.location, protocol='jsonrpc+ssl', port=443)
    #         api = odoo.login(
    #             'ssttest9',
    #             self._location.username,
    #             self._location.password
    #         )
    #         api.__enter__()
    #         self._api = api
    #     return self._api

    def __enter__(self):
        # do nothing here
        return self

    def __exit__(self, type, value, traceback):
        # if self._api is not None:
        #     self._api.__exit__(type, value, traceback)
        # odoo = odoorpc.ODOO(self._location.location, protocol='jsonrpc+ssl', port=443)
        # odoo.logout()
        self._odoo.logout()

    def call(self, model, method, arguments):
        odoo = self._odoo
        try:
            # When Magento is installed on PHP 5.4+, the API
            # may return garble data if the arguments contain
            # trailing None.
            if isinstance(arguments, list):
                while arguments and arguments[-1] is None:
                    arguments.pop()
            start = datetime.now()
            try:
                # result = self.api.call(method, arguments)
                odoo.login(
                    'ssttest11',
                    self._location.username,
                    self._location.password
                )
                if method == 'search':
                    # result = odoo.env[method].search([('write_date', '>=', '2018-08-01 00:00:00'), ('write_date', '<=', '2018-08-13 23:59:59')])
                    odoo_field = next(iter(arguments[0]))
                    # result = odoo.env[method].search([(odoo_field, '>=', '2018-08-01 00:00:00'), (odoo_field, '<=', '2018-08-13 23:59:59')])
                    result = odoo.env[model].search([(odoo_field, '>=', arguments[0][odoo_field]['from']), (odoo_field, '<=', arguments[0][odoo_field]['to'])])
                if method == 'read':
                    result = odoo.env[model].read(arguments)[0] # return dict
            except:
                _logger.error("api.call('%s', %s) failed", method,
                              arguments)
                raise
            else:
                _logger.debug(
                    "api.call('%s', %s) returned %s in %s seconds",
                    method, arguments, result,
                    (datetime.now() - start).seconds)
            # Uncomment to record requests/responses in ``recorder``
            # record(method, arguments, result)
            return result
        except (socket.gaierror, socket.error, socket.timeout) as err:
            raise NetworkRetryableError(
                'A network error caused the failure of the job: '
                '%s' % err)
        except xmlrpc.client.ProtocolError as err:
            if err.errcode in [502,  # Bad gateway
                               503,  # Service unavailable
                               504]:  # Gateway timeout
                raise RetryableJobError(
                    'A protocol error caused the failure of the job:\n'
                    'URL: %s\n'
                    'HTTP/HTTPS headers: %s\n'
                    'Error code: %d\n'
                    'Error message: %s\n' %
                    (err.url, err.headers, err.errcode, err.errmsg))
            else:
                raise

# class MagentoAPI(object):
#
#     def __init__(self, location):
#         """
#         :param location: Magento location
#         :type location: :class:`MagentoLocation`
#         """
#         self._location = location
#         self._api = None
#
#     @property
#     def api(self):
#         if self._api is None:
#             custom_url = self._location.use_custom_api_path
#             api = magentolib.API(
#                 self._location.location,
#                 self._location.username,
#                 self._location.password,
#                 full_url=custom_url
#             )
#             api.__enter__()
#             self._api = api
#         return self._api
#
#     def __enter__(self):
#         # we do nothing, api is lazy
#         return self
#
#     def __exit__(self, type, value, traceback):
#         if self._api is not None:
#             self._api.__exit__(type, value, traceback)
#
#     def call(self, method, arguments):
#         try:
#             # When Magento is installed on PHP 5.4+, the API
#             # may return garble data if the arguments contain
#             # trailing None.
#             if isinstance(arguments, list):
#                 while arguments and arguments[-1] is None:
#                     arguments.pop()
#             start = datetime.now()
#             try:
#                 result = self.api.call(method, arguments)
#             except:
#                 _logger.error("api.call('%s', %s) failed", method, arguments)
#                 raise
#             else:
#                 _logger.debug("api.call('%s', %s) returned %s in %s seconds",
#                               method, arguments, result,
#                               (datetime.now() - start).seconds)
#             # Uncomment to record requests/responses in ``recorder``
#             # record(method, arguments, result)
#             return result
#         except (socket.gaierror, socket.error, socket.timeout) as err:
#             raise NetworkRetryableError(
#                 'A network error caused the failure of the job: '
#                 '%s' % err)
#         except xmlrpc.client.ProtocolError as err:
#             if err.errcode in [502,   # Bad gateway
#                                503,   # Service unavailable
#                                504]:  # Gateway timeout
#                 raise RetryableJobError(
#                     'A protocol error caused the failure of the job:\n'
#                     'URL: %s\n'
#                     'HTTP/HTTPS headers: %s\n'
#                     'Error code: %d\n'
#                     'Error message: %s\n' %
#                     (err.url, err.headers, err.errcode, err.errmsg))
#             else:
#                 raise


class OdooCRUDAdapter(AbstractComponent):
    """ External Records Adapter for Odoo """

    _name = 'odoo.crud.adapter'
    _inherit = ['base.backend.adapter', 'base.odoo.connector']
    _usage = 'backend.adapter'

    def search(self, filters=None):
        """ Search records according to some criterias
        and returns a list of ids """
        raise NotImplementedError

    def read(self, id, attributes=None):

        """ Returns the information of a record """
        raise NotImplementedError

    def search_read(self, filters=None):
        """ Search records according to some criterias
        and returns their information"""
        raise NotImplementedError

    def create(self, data):
        """ Create a record on the external system """
        raise NotImplementedError

    def write(self, id, data):
        """ Update records on the external system """
        raise NotImplementedError

    def delete(self, id):
        """ Delete a record on the external system """
        raise NotImplementedError

    def _call(self, model, method, arguments):
        try:
            odoo_api = getattr(self.work, 'odoo_api')
        except AttributeError:
            raise AttributeError(
                'You must provide a odoo_api attribute with a '
                'OdooAPI instance to be able to use the '
                'Backend Adapter.'
            )
        return odoo_api.call(model, method, arguments)


class GenericAdapter(AbstractComponent):

    _name = 'odoo.adapter'
    _inherit = 'odoo.crud.adapter'

    _magento_model = None
    _admin_path = None

    def search(self, filters=None):
        """ Search records according to some criterias
        and returns a list of ids

        :rtype: list
        """
        return self._call('%s.search' % self._magento_model,
                          [filters] if filters else [{}])

    def read(self, id, attributes=None):
        """ Returns the information of a record

        :rtype: dict
        """
        arguments = [int(id)]
        if attributes:
            # Avoid to pass Null values in attributes. Workaround for
            # https://bugs.launchpad.net/openerp-connector-magento/+bug/1210775
            # When Magento is installed on PHP 5.4 and the compatibility patch
            # http://magento.com/blog/magento-news/magento-now-supports-php-54
            # is not installed, calling info() with None in attributes
            # would return a wrong result (almost empty list of
            # attributes). The right correction is to install the
            # compatibility patch on Magento.
            arguments.append(attributes)
        return self._call('%s.info' % self._magento_model,
                          arguments)

    def search_read(self, filters=None):
        """ Search records according to some criterias
        and returns their information"""
        return self._call('%s.list' % self._magento_model, [filters])

    def create(self, data):
        """ Create a record on the external system """
        return self._call('%s.create' % self._magento_model, [data])

    def write(self, id, data):
        """ Update records on the external system """
        return self._call('%s.update' % self._magento_model,
                          [int(id), data])

    def delete(self, id):
        """ Delete a record on the external system """
        return self._call('%s.delete' % self._magento_model, [int(id)])

    def admin_url(self, id):
        """ Return the URL in the Magento admin for a record """
        if self._admin_path is None:
            raise ValueError('No admin path is defined for this record')
        backend = self.backend_record
        url = backend.admin_location
        if not url:
            raise ValueError('No admin URL configured on the backend.')
        path = self._admin_path.format(model=self._magento_model,
                                       id=id)
        url = url.rstrip('/')
        path = path.lstrip('/')
        url = '/'.join((url, path))
        return url
