odoo.define('website_paynow_hide.website_paynow', function (require) {
    'use strict';
    require('website.website');
    require('web.dom_ready');
    console.log(":::::::::::body------------------",$("#wrap"))
    $('#o_payment_form_pay').on('click',function(ev){
        if ($(".o_payment_form").find('div.panel-body').find('input[type="radio"]:checked').length != 0){
            $("#wrap").addClass("loading");
        }
    });

});
