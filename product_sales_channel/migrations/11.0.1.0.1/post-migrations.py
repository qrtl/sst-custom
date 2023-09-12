# Copyright 2023 Quartile Limited

from openupgradelib import openupgrade

MODULE_LIST = ["product_ext_sst"]
fields_list = ["team_ids"]


@openupgrade.migrate()
def migrate(env, version):
    # Update the module reference in external identifiers
    for field in fields_list:
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE ir_model_data
            SET module = 'product_sales_channel'
            WHERE module IN %s AND model = 'ir.model.fields' and name LIKE %s;
            """,
            (
                tuple(MODULE_LIST),
                "%" + field + "%",
            ),
        )
