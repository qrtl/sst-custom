# Copyright 2023 Quartile Limited

from openupgradelib import openupgrade

MODULE_LIST = ["purchase_ext_sst"]
fields_list = ["%purchase_category_id%"]
model_list = ["%purchase_category%"]

@openupgrade.migrate()
def migrate(env, version):
    # Update the module reference in external identifiers
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_model_data
        SET module = 'purchase_order_category'
        WHERE module IN %s AND model = 'ir.model.fields' and name LIKE %s;
        """,
        (tuple(MODULE_LIST),fields_list,)
    )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_model_data
        SET module = 'purchase_order_category'
        WHERE module IN %s AND model = 'ir.model.fields' and name LIKE %s;
        """,
        (tuple(MODULE_LIST), model_list,)
    )

    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_model_data
        WHERE module IN %s AND model = ('ir.model') and name LIKE %s;
        """,
        (tuple(MODULE_LIST), model_list,)
    )

    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_model_data
        WHERE module IN %s AND model = ('purchase.category') and name LIKE %s;
        """,
        (tuple(MODULE_LIST), model_list,)
    )
