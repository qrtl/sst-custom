# Copyright 2023 Quartile Limited

from openupgradelib import openupgrade

MODULE_LIST = ["purchase_ext_sst"]
fields_list = ["request_channel_id", "request_medium_id"]
model_list = ["request_channel", "request_medium"]


@openupgrade.migrate()
def migrate(env, version):
    # Update the module reference in external identifiers
    for field in fields_list:
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE ir_model_data
            SET module = 'purchase_order_channel'
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
            SET module = 'purchase_order_channel'
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
            WHERE module IN %s AND model = 'request.channel' and name LIKE %s;
            """,
            (
                tuple(MODULE_LIST),
                "%" + model + "%",
            ),
        )
