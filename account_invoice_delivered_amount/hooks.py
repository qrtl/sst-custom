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
            ADD COLUMN "amount_total_delivered" numeric,
            ADD COLUMN "amount_total_delivered_signed" numeric,
            ADD COLUMN "delivery_done" bool
        """
        )
    if not column_exists(cr, "account_invoice_line", "is_delivered"):
        cr.execute(
            """
            ALTER TABLE "account_invoice_line"
            ADD COLUMN "is_delivered" bool,
            ADD COLUMN "delivered_amount" numeric
        """
        )
