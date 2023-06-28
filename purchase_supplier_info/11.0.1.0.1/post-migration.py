# # Copyright 2023 Quartile Limited

# from openupgradelib import openupgrade

# MODULE_LIST = ["purchase_ext_sst"]
# fields_list = ["purchase_ext_sst_phone_update", "purchase_ext_sst_mobile_update", 
# "purchase_ext_sst_phone_search", "purchase_ext_sst_supplier_phone", 
# "purchase_ext_sst_supplier_mobile","purchase_ext_sst_tentative_name",]

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

