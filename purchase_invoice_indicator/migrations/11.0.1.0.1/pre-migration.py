from openupgradelib import openupgrade

@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, [
        ('account.invoice', 'account_invoice', 'is_invoice', 'is_invoice_issuer'),
    ])
