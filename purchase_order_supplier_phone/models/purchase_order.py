# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    phone_update = fields.Char()
    mobile_update = fields.Char()
    phone_search = fields.Char(
        states={
            "purchase": [("readonly", True)],
            "done": [("readonly", True)],
            "cancel": [("readonly", True)],
        },
    )
    supplier_phone = fields.Char(
        related="partner_id.phone",
        string="Supplier Phone",
        readonly=True,
        store=True,
    )
    supplier_mobile = fields.Char(
        related="partner_id.mobile",
        string="Supplier Mobile",
        readonly=True,
        store=True,
    )
    tentative_name = fields.Char("Tentative Name")

    @api.multi
    def write(self, vals):
        # Propose supplier logic
        if (
            "phone_search" in vals
            or "phone_update" in vals
            or "mobile_update" in vals
            or "tentative_name" in vals
        ):
            val_phone_search = "phone_search" in vals and vals["phone_search"] or False
            val_phone = "phone_update" in vals and vals["phone_update"] or False
            val_mobile = "mobile_update" in vals and vals["mobile_update"] or False
            for order in self:
                val_tent_name = (
                    "tentative_name" in vals
                    and vals["tentative_name"]
                    or order.tentative_name
                )
                partner_id = (
                    "partner_id" in vals and vals["partner_id"] or order.partner_id.id
                )
                if self.is_default_partner(partner_id) and (
                    val_phone or val_mobile or val_phone_search
                ):
                    partner_id = self.create_partner(
                        val_phone or val_phone_search, val_mobile
                    ).id
                if not self.is_default_partner(partner_id):
                    partner = self.env["res.partner"].browse(partner_id)
                    self.update_partner(partner, val_phone, val_mobile, val_tent_name)
                vals["partner_id"] = partner_id
            vals["phone_update"] = vals["mobile_update"] = False
        return super(PurchaseOrder, self).write(vals)

    @api.model
    def create(self, vals):
        val_phone_search = "phone_search" in vals and vals["phone_search"] or False
        val_phone = "phone_update" in vals and vals["phone_update"] or False
        val_mobile = "mobile_update" in vals and vals["mobile_update"] or False
        val_tent_name = "tentative_name" in vals and vals["tentative_name"] or False
        if self.is_default_partner(vals["partner_id"]) and (
            val_phone or val_mobile or val_phone_search
        ):
            vals["partner_id"] = self.create_partner(
                val_phone or val_phone_search, val_mobile
            ).id
        if not self.is_default_partner(vals["partner_id"]):
            partner = self.env["res.partner"].browse(vals["partner_id"])
            self.update_partner(partner, val_phone, val_mobile, val_tent_name)
        vals["phone_update"] = vals["mobile_update"] = False
        return super(PurchaseOrder, self).create(vals)

    def create_partner(self, phone, mobile):
        partner = self.env["res.partner"].create(
            {
                "name": "未確認",
                "phone": phone,
                "mobile": mobile,
                "supplier": True,
                "customer": False,
            }
        )
        return partner

    def update_partner(self, partner, phone, mobile, tent_name):
        if phone and partner.phone != phone:
            partner.phone = phone
        if mobile and partner.mobile != mobile:
            partner.mobile = mobile
        if tent_name and partner.name != tent_name:
            partner.name = tent_name

    @api.onchange("phone_search")
    def onchange_phone_search(self):
        if self.phone_search:
            self.phone_update = False
            self.mobile_update = False
            partner = self.get_partner_from_phone(self.phone_search)
            if partner:
                self.partner_id = partner
            elif self.partner_id:
                if self.is_default_partner(self.partner_id.id):
                    self.phone_update = self.phone_search

    @api.onchange("phone_update")
    def onchange_phone_update(self):
        if self.phone_update:
            return self.check_onchange_phone(self.phone_update, "phone_update")

    @api.onchange("mobile_update")
    def onchange_mobile_update(self):
        if self.mobile_update:
            return self.check_onchange_phone(self.mobile_update, "mobile_update")

    def check_onchange_phone(self, phone, field):
        try:
            partner = self.get_partner_from_phone(phone)
            if self.partner_id and partner and partner != self.partner_id:
                conflicts_user = _("\n%s\n- Phone: %s\n- Mobile: %s\n") % (
                    partner.name,
                    partner.phone or "",
                    partner.mobile or "",
                )
                return {
                    "warning": {
                        "message": _(
                            "The entered phone (%s) conflicts with "
                            "the following user(s):\n%s"
                        )
                        % (phone or "N/A", conflicts_user)
                    },
                    "value": {field: False},
                }
        except UserError as e:
            return {"warning": {"message": e.name}, "value": {field: False}}

    def get_partner_from_phone(self, phone):
        Partner = self.env["res.partner"]
        partners = False
        # here we use "or" condition instead of "and"
        if phone:
            partners = Partner.search(
                [
                    "|",
                    ("phone", "=", phone),
                    ("mobile", "=", phone),
                    ("active", "=", True),
                    ("supplier", "=", True),
                ]
            )
        if partners and len(partners) > 1:
            conflicts_users_list = ""
            for partner in partners:
                conflicts_users_list += _("\n%s\n- Phone: %s\n- " "Mobile: %s\n") % (
                    partner.name,
                    partner.phone or "",
                    partner.mobile or "",
                )
            raise UserError(
                _("The entered phone (%s) " "conflicts with the following user(s):\n%s")
                % (phone or "N/A", conflicts_users_list)
            )
        return partners if partners else False
