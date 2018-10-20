import openerp.addons.connector.backend as backend

odoo_external = backend.Backend('odoo_external')
""" Generic odoo_external Backend """

odoo_externalv11 = backend.Backend(parent=odoo_external, version='v11')
""" odoo_external Backend for version v11 """
