# Copyright 2013-2017 Camptocamp SA
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import base64
import logging
import sys
import urllib.request

from odoo import _

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping

# from ...components.mapper import normalize_datetime

_logger = logging.getLogger(__name__)


class ProductBatchImporter(Component):
    """ Import the Odoo Products.

    For every product category in the list, a delayed job is created.
    Import from a date
    """

    _name = "odoo.product.product.batch.importer"
    _inherit = "odoo.delayed.batch.importer"
    _apply_on = ["odoo.product.product"]

    def run(self, filters=None):
        """ Run the synchronization """
        from_date = filters.pop("from_date", None)
        to_date = filters.pop("to_date", None)
        external_ids = self.backend_adapter.search(
            filters, from_date=from_date, to_date=to_date
        )
        _logger.info("search for odoo products %s returned %s", filters, external_ids)
        for external_id in external_ids:
            self._import_record(external_id)


class CatalogImageImporter(Component):
    """ Import images for a record.

    Usually called from importers, in ``_after_import``.
    For instance from the products importer.
    """

    _name = "odoo.product.image.importer"
    _inherit = "odoo.importer"
    _apply_on = ["odoo.product.product"]
    _usage = "product.image.importer"

    def _get_images(self, storeview_id=None):
        return self.backend_adapter.get_images(self.external_id, storeview_id)

    def _sort_images(self, images):
        """ Returns a list of images sorted by their priority.
        An image with the 'image' type is the the primary one.
        The other images are sorted by their position.

        The returned list is reversed, the items at the end
        of the list have the higher priority.
        """
        if not images:
            return {}

        # place the images where the type is 'image' first then
        # sort them by the reverse priority (last item of the list has
        # the the higher priority)

        def priority(image):
            primary = "image" in image["types"]
            try:
                position = int(image["position"])
            except ValueError:
                position = sys.maxsize
            return (primary, -position)

        return sorted(images, key=priority)

    def _get_binary_image(self, image_data):
        url = image_data["url"].encode("utf8")
        try:
            request = urllib.request.Request(url)
            if (
                self.backend_record.auth_basic_username
                and self.backend_record.auth_basic_password
            ):
                base64string = base64.b64encode(
                    "%s:%s"
                    % (
                        self.backend_record.auth_basic_username,
                        self.backend_record.auth_basic_password,
                    )
                )
                request.add_header("Authorization", "Basic %s" % base64string)
            binary = urllib.request.urlopen(request)
        except urllib.request.HTTPError as err:
            if err.code == 404:
                # the image is just missing, we skip it
                return
            else:
                # we don't know why we couldn't download the image
                # so we propagate the error, the import will fail
                # and we have to check why it couldn't be accessed
                raise
        else:
            return binary.read()

    def _write_image_data(self, binding, binary, image_data):
        binding = binding.with_context(connector_no_export=True)
        binding.write({"image": base64.b64encode(binary)})

    def run(self, external_id, binding):
        self.external_id = external_id
        images = self._get_images()
        images = self._sort_images(images)
        binary = None
        image_data = None
        while not binary and images:
            image_data = images.pop()
            binary = self._get_binary_image(image_data)
        if not binary:
            return
        self._write_image_data(binding, binary, image_data)


# TODO: not needed, use inheritance
class BundleImporter(Component):
    """ Can be inherited to change the way the bundle products are
    imported.

    Called at the end of the import of a product.

    Example of action when importing a bundle product:
        - Create a bill of material
        - Import the structure of the bundle in new objects

    By default, the bundle products are not imported: the jobs
    are set as failed, because there is no known way to import them.
    An additional module that implements the import should be installed.

    If you want to create a custom importer for the bundles, you have to
    inherit the Component::

        class BundleImporter(Component):
            _inherit = 'odoo.product.bundle.importer'

    And to add the bundle type in the supported product types::

        class OdooProductProduct(models.Model):
            _inherit = 'odoo.product.product'

            @api.model
            def product_type_get(self):
                types = super(OdooProductProduct, self).product_type_get()
                if 'bundle' not in [item[0] for item in types]:
                    types.append(('bundle', 'Bundle'))
                return types

    """

    _name = "odoo.product.bundle.importer"
    _inherit = "odoo.importer"
    _apply_on = ["odoo.product.product"]
    _usage = "product.bundle.importer"

    def run(self, binding, odoo_record):
        """ Import the bundle information about a product.

        :param odoo_record: product information from Odoo
        """


class ProductImportMapper(Component):
    _name = "odoo.product.product.import.mapper"
    _inherit = "odoo.import.mapper"
    _apply_on = ["odoo.product.product"]

    # TODO :     categ, special_price => minimal_price
    direct = [
        ("name", "name"),
        ("description", "description"),
        ("weight", "weight"),
        # ('cost', 'standard_price'),
        # ('short_description', 'description_sale'),
        # ('sku', 'default_code'),
        # ('type_id', 'product_type'),
        ("standard_price", "standard_price"),
        ("description_sale", "description_sale"),
        ("default_code", "default_code"),
        ("type", "type"),
        # (normalize_datetime('created_at'), 'created_at'),
        # (normalize_datetime('updated_at'), 'updated_at'),
        ("created_date", "create_date"),
        ("write_date", "write_date"),
    ]

    @mapping
    def is_active(self, record):
        """Check if the product is active in Odoo
        and set active flag in OpenERP
        status == 1 in Odoo means active"""
        return {"active": (record.get("status") == "1")}

    @mapping
    def price(self, record):
        return {"list_price": record.get("price", 0.0)}

    @mapping
    def categories(self, record):
        result = {}
        # Use the default category
        result["categ_id"] = self.backend_record.default_category_id.id
        return result

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}


class ProductImporter(Component):
    _name = "odoo.product.product.importer"
    _inherit = "odoo.importer"
    _apply_on = ["odoo.product.product"]

    def _import_bundle_dependencies(self):
        """ Import the dependencies for a Bundle """
        bundle = self.odoo_record["_bundle_data"]
        for option in bundle["options"]:
            for selection in option["selections"]:
                self._import_dependency(selection["product_id"], "odoo.product.product")

    def _must_skip(self):
        """ Hook called right after we read the data from the backend.

        If the method returns a message giving a reason for the
        skipping, the import will be interrupted and the message
        recorded in the job (if the import is called directly by the
        job, not by dependencies).

        If it returns None, the import will continue normally.

        :returns: None | str | unicode
        """
        if self.odoo_record["type"] == "service":
            return _("Service product is not imported into Odoo " "(out of scope).")

    def _validate_data(self, data):
        """ Check if the values to import are correct

        Pro-actively check before the ``_create`` or
        ``_update`` if some fields are missing or invalid

        Raise `InvalidDataError`
        """
        return

    def _create(self, data):
        binding = super(ProductImporter, self)._create(data)
        self.backend_record.add_checkpoint(binding)
        return binding

    def _after_import(self, binding):
        """ Hook called at the end of the import """
        translation_importer = self.component(usage="translation.importer",)
        translation_importer.run(
            self.external_id, binding, mapper="odoo.product.product.import.mapper"
        )
        image_importer = self.component(usage="product.image.importer")
        image_importer.run(self.external_id, binding)

        if self.odoo_record["type_id"] == "bundle":
            bundle_importer = self.component(usage="product.bundle.importer")
            bundle_importer.run(binding, self.odoo_record)


class ProductInventoryExporter(Component):
    _name = "odoo.product.product.exporter"
    _inherit = "odoo.exporter"
    _apply_on = ["odoo.product.product"]
    _usage = "product.inventory.exporter"

    _map_backorders = {
        "use_default": 0,
        "no": 0,
        "yes": 1,
        "yes-and-notification": 2,
    }

    def _get_data(self, binding, fields):
        result = {}
        if "odoo_qty" in fields:
            result.update(
                {
                    "qty": binding.odoo_qty,
                    # put the stock availability to "out of stock"
                    "is_in_stock": int(binding.odoo_qty > 0),
                }
            )
        if "manage_stock" in fields:
            manage = binding.manage_stock
            result.update(
                {
                    "manage_stock": int(manage == "yes"),
                    "use_config_manage_stock": int(manage == "use_default"),
                }
            )
        if "backorders" in fields:
            backorders = binding.backorders
            result.update(
                {
                    "backorders": self._map_backorders[backorders],
                    "use_config_backorders": int(backorders == "use_default"),
                }
            )
        return result

    def run(self, binding, fields):
        """ Export the product inventory to Odoo """
        external_id = self.binder.to_external(binding)
        data = self._get_data(binding, fields)
        self.backend_adapter.update_inventory(external_id, data)
