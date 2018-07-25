from openerp import models, fields
from openerp.addons.connector.connector import (ConnectorEnvironment,
                                                install_in_connector)
from openerp.addons.connector.checkpoint import checkpoint

install_in_connector()


def get_environment(session, model_name, backend_id):
    """ Create an environment to work with.  """
    backend_record = session.env['odoo_external.backend'].browse(backend_id)
    env = ConnectorEnvironment(backend_record, session, model_name)
    lang = backend_record.default_lang_id
    lang_code = lang.code if lang else 'en_US'
    if lang_code == session.context.get('lang'):
        return env
    else:
        with env.session.change_context(lang=lang_code):
            return env


class OdooExternalBinding(models.AbstractModel):

    """ Abstract Model for the Bindigs.

    All the models used as bindings between WooCommerce and OpenERP
    (``woo.res.partner``, ``woo.product.product``, ...) should
    ``_inherit`` it.
    """
    _name = 'odoo_external.binding'
    _inherit = 'external.binding'
    _description = 'odoo_external Binding (abstract)'

    # openerp_id = openerp-side id must be declared in concrete model
    backend_id = fields.Many2one(
        comodel_name='odoo_external.backend',
        string='Woo Backend',
        required=True,
        ondelete='restrict',
    )
    # fields.Char because 0 is a valid WooCommerce ID
    odoo_external_id = fields.Char(string='ID on Woo')

    _sql_constraints = [
        ('odoo_external_uniq', 'unique(backend_id, odoo_external_id)',
         'A binding already exists with the same odoo_external ID.'),
    ]


def add_checkpoint(session, model_name, record_id, backend_id):
    """ Add a row in the model ``connector.checkpoint`` for a record,
    meaning it has to be reviewed by a user.

    :param session: current session
    :type session: :class:`openerp.addons.connector.session.ConnectorSession`
    :param model_name: name of the model of the record to be reviewed
    :type model_name: str
    :param record_id: ID of the record to be reviewed
    :type record_id: int
    :param backend_id: ID of the WooCommerce Backend
    :type backend_id: int
    """
    return checkpoint.add_checkpoint(session, model_name, record_id,
                                     'odoo_external.backend', backend_id)
