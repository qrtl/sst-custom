# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tools import column_exists


def pre_init_hook(cr):
    """Allow installing the module in a database with large account.invoice and
    account.invoice.line tables by skipping the computation.
    """
    if not column_exists(cr, "account_invoice", "total_delivered_amount"):
        cr.execute(
            """
            ALTER TABLE "account_invoice"
            ADD COLUMN "total_delivered_amount" numeric,
            ADD COLUMN "total_delivered_amount_signed" numeric
        """
        )
    if not column_exists(cr, "account_invoice_line", "is_delivered"):
        cr.execute(
            """
            ALTER TABLE "account_invoice_line"
            ADD COLUMN "is_delivered" bool,
            ADD COLUMN "deliverd_amount" numeric
        """
        )
