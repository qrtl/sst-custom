# Copyright 2023 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade

MODULE_LIST = ["product_ext_sst"]
fields_list = ["product_state_id"]
model_list = ["product_state"]


@openupgrade.migrate()
def migrate(env, version):
    # Update the module reference in external identifiers
    for field in fields_list:
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE ir_model_data
            SET module = 'product_state'
            WHERE module IN %s AND model = 'ir.model.fields' and name LIKE %s;
            """,
            (
                tuple(MODULE_LIST),
                "%" + field + "%",
            ),
        )
    for model in model_list:
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE ir_model_data
            SET module = 'product_state'
            WHERE module IN %s AND model = 'ir.model.fields' and name LIKE %s;
            """,
            (
                tuple(MODULE_LIST),
                "%" + model + "%",
            ),
        )
        openupgrade.logged_query(
            env.cr,
            """
            DELETE FROM ir_model_data
            WHERE module IN %s AND model = ('ir.model') and name LIKE %s;
            """,
            (
                tuple(MODULE_LIST),
                "%" + model + "%",
            ),
        )
        openupgrade.logged_query(
            env.cr,
            """
            DELETE FROM ir_model_data
            WHERE module IN %s AND model = ('product.state') and name LIKE %s;
            """,
            (
                tuple(MODULE_LIST),
                "%" + model + "%",
            ),
        )
