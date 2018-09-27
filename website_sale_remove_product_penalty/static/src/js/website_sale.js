odoo.define('cart_update_confirm', function (require) {
    'use strict';
    require('website.website');

    $(document).ready(function(e){
        $('.js_delete_product_cart_update').hide();
        $('.oe_website_spinner_cart_update').hide();
        $('.cart_update_confirm').click(function() {
            $('.js_delete_product_cart_update').show();
            $('.oe_website_spinner_cart_update').show();
            $('#cart_update_confirm').hide();
            $(".span_js_product_qty").hide();
        });
    });
});
