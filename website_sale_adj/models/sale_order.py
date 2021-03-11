# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.osv import expression

from odoo.addons.queue_job.job import job


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Store the earilest website_order_line's creation date
    order_line_date = fields.Datetime(
        "Order Date", compute="_compute_order_line_date", store=True,
    )

    @api.multi
    @api.depends("order_line")
    def _compute_order_line_date(self):
        for order in self:
            website_order_line = order.website_order_line
            order.order_line_date = (
                website_order_line[0].create_date if website_order_line else False
            )

    # Since quotation will be created after checked, use order_line_date to
    # compute is_abandoned_cart field instead of date_order
    @api.multi
    @api.depends(
        "team_id.team_type", "order_line_date", "order_line", "state", "partner_id"
    )
    def _compute_abandoned_cart(self):
        abandoned_delay = float(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website_sale.cart_abandoned_delay", "1.0")
        )
        abandoned_datetime = fields.Datetime.to_string(
            datetime.utcnow() - relativedelta(hours=abandoned_delay)
        )
        for order in self:
            domain = (
                order.order_line_date
                and order.order_line_date <= abandoned_datetime
                and order.team_id.team_type == "website"
                and order.state == "draft"
                and order.partner_id.id != self.env.ref("base.public_partner").id
                and order.order_line
            )
            order.is_abandoned_cart = bool(domain)

    def _search_abandoned_cart(self, operator, value):
        abandoned_delay = float(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website_sale.cart_abandoned_delay", "1.0")
        )
        abandoned_datetime = fields.Datetime.to_string(
            datetime.utcnow() - relativedelta(hours=abandoned_delay)
        )
        abandoned_domain = expression.normalize_domain(
            [
                ("order_line_date", "<=", abandoned_datetime),
                ("team_id.team_type", "=", "website"),
                ("state", "=", "draft"),
                ("partner_id", "!=", self.env.ref("base.public_partner").id),
                ("order_line", "!=", False),
            ]
        )
        # is_abandoned domain possibilities
        if (operator not in expression.NEGATIVE_TERM_OPERATORS and value) or (
            operator in expression.NEGATIVE_TERM_OPERATORS and not value
        ):
            return abandoned_domain
        return expression.distribute_not(abandoned_domain)  # negative domain

    # Overwrite force_quotation_send and put the email
    # in queue instead of sending it immediately
    @api.multi
    def force_quotation_send(self):
        for order in self:
            email_act = order.action_quotation_send()
            if email_act and email_act.get("context"):
                email_ctx = email_act["context"]
                email_ctx.update(default_email_from=order.company_id.email)
                email_ctx["email_bcc"] = ",".join(
                    [str(partner.email) for partner in order.message_partner_ids]
                )
                email_ctx["reply_to"] = order.message_get_reply_to(
                    [order.id], default=email_ctx["default_email_from"]
                )[order.id]
                order.with_delay(
                    description="%s: Send Order Confirmation Email" % order.name
                ).send_confirmation_email(email_ctx)
                if (
                    "mark_so_as_sent" in email_ctx
                    and email_ctx["mark_so_as_sent"]
                    and order.state == "draft"
                ):
                    order.with_context(tracking_disable=True).state = "sent"
        return True

    @job()
    def send_confirmation_email(self, email_ctx):
        self.with_context(email_ctx).message_post_with_template(
            email_ctx.get("default_template_id")
        )
