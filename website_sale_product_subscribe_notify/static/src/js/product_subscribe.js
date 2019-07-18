odoo.define('website_sale_product_subscribe_notify.product_subscribe', function (require) {
    'use strict';

    require('web.dom_ready');
    var website = require('website.website');
    var ajax = require('web.ajax');

    $("i[name='plus_circle']").parents('li').find('ul:first').hide()

    $("i[name='cross_circle']").hide()

    $("i[name='plus_circle']").on('click', function (el) {
        $(this).parent().find('i.fa-times-circle').show();
        var li = $(this).parents('li').find('ul').show();
        $(this).hide();
    });

    $("i[name='cross_circle']").on('click', function (el) {
        $(this).parent().find('i.fa-plus-circle').show();
        var li = $(this).parents('li').find('ul').hide();
        $(this).hide();
    });

    $("input[name='categ_subscribe']").on('click', function (el) {
        var checked = $(this).prop('checked')
        $(this).parent().find('input').prop('checked', checked)
    });


});
