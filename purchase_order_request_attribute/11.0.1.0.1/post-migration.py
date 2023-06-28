# # Copyright 2023 Quartile Limited

# from openupgradelib import openupgrade

# MODULE_LIST = ["purchase_ext_sst"]
# fields_list = ["purchase_ext_sst_request_channel_id", "purchase_ext_sst_request_medium_id"]

# @openupgrade.migrate()
# def migrate(env, version):
#     # Update the module reference in external identifiers
#     openupgrade.logged_query(
#         env.cr,
#         """
#         UPDATE ir_model_data
#         SET module = 'purchase_order_category'
#         WHERE module IN %s AND model = 'ir.model.fields' and name in %s;
#         """,
#         (tuple(MODULE_LIST),(tuple(fields_list),))
#     )

