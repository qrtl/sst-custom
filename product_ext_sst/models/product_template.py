# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    team_ids = fields.Many2many(
        "crm.team",
        "product_tmpl_team_rel",
        "product_tmpl_id",
        "team_id",
        "Sales Channels",
    )
    manufacturer = fields.Char()
    manufactured_year = fields.Selection(
        [(num, str(num)) for num in reversed(range(1900, datetime.now().year + 1))],
        "Manufactured Year",
    )
    model = fields.Char()
    product_state_id = fields.Many2one("product.state", "Product State")
    purchase_category_id = fields.Many2one("purchase.category", "Purchase Category",)
    evaluated_by_id = fields.Many2one("hr.employee", "Evaluated By")
    purchased_by_id = fields.Many2one("hr.employee", "Purchased By")
    shop_id = fields.Many2one("stock.warehouse", string="Shop Purchased")
    list_price = fields.Float(track_visibility="onchange")

    @api.multi
    def open_record(self):
        form_id = self.env.ref("product.product_template_only_form_view")
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "res_id": self.id,
            "view_type": "form",
            "view_mode": "form",
            "view_id": form_id.id,
            "context": {},
            "target": "current",
        }

    @api.model
    def create(self, vals):
        defaults = self.env["product.template"].default_get(["list_price"])
        if "list_price" not in vals or vals["list_price"] == defaults["list_price"]:
            if "product_state_id" in vals:
                list_price = self.get_propose_list_price(
                    vals["name"], vals["product_state_id"]
                )
            else:
                list_price = self.get_propose_list_price(vals["name"])
            if list_price:
                vals["list_price"] = list_price
        return super(ProductTemplate, self).create(vals)

    def action_propose_list_price(self):
        if self.product_state_id:
            list_price = self.get_propose_list_price(
                self.name, self.product_state_id.id
            )
        else:
            list_price = self.get_propose_list_price(self.name)
        if list_price:
            self.list_price = list_price

    def get_propose_list_price(self, name, state=False):
        query = """
            SELECT
                price
            FROM
                product_price_record
            WHERE
                %s LIKE '%%' || string || '%%'
        """
        query_param = [name]
        if state:
            query += """
            AND
                product_state_id = %s
            """
            query_param.append(state)
        query += """
            ORDER BY CHAR_LENGTH(string) DESC
            LIMIT 1;
        """
        self.env.cr.execute(query, query_param)
        result = self.env.cr.fetchone()
        return result[0] if result else False
