/* Copyright 2018 Soliton Systems
 * Copyright 2018 Alliance Software Inc.
 * Copyright 2018 Quartile Limited
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).*/

odoo.define("website_payment_loading.website_payment", function(require) {
  "use strict";
  require("website.website");
  require("web.dom_ready");
  $("#o_payment_form_pay").on("click", function(ev) {
    if (
      $(".o_payment_form")
        .find("div.panel-body")
        .find('input[type="radio"]:checked').length != 0
    ) {
      $("#wrap").addClass("loading");
    }
  });
});
