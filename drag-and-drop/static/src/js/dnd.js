/*
Copyright (C) Andreas Wyrobek - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Andreas Wyrobek <andreas.wyrobek95@gmail.com>, December 2017
*/

odoo.define('dragndrop.dragndrop', function (require) {
"use strict";

require('web.dom_ready');
var core = require('web.core');
var Dialog = require('web.Dialog');
var framework = require('web.framework');
var Sidebar = require('web.Sidebar');
var FormRenderer = require('web.FormRenderer');
var FormController = require('web.FormController');
var Chatter = require('mail.Chatter');
var Composer = require('mail.composer');
var session = require('web.session');

var _t = core._t;

function initDnd($form, $dnd, callback) {
       var droppedFiles = false;
       var tid = null;
       $form.on('dragover dragenter', function(ev) {
         clearTimeout(tid);
         ev.stopPropagation();
         ev.preventDefault();
         $dnd.removeClass('dnd-hidden');
       })
       .on('dragleave drop', function(ev) {
           tid = setTimeout(function(){
                ev.stopPropagation();
                $dnd.addClass('dnd-hidden');
           }, 50);
       })
       .on('drop', function(ev) {
         ev.stopPropagation();
         ev.preventDefault();
         $dnd.addClass('dnd-hidden');
         droppedFiles = ev.originalEvent.dataTransfer.files;
         callback(droppedFiles);
       });
};

function uploadAttachment($uploadform, files, trigger, setIdToZero) {
    var count = 0;
    var tocount = 0;
    for(var f in files){
        if(typeof files[f] === 'object') tocount++;
    }

    if(tocount>0) {
        framework.blockUI();
    }

    for(var f in files){
        var file = files[f];
        if(typeof file !== 'object') return;
        var serializeArray = $uploadform.serializeArray();
        var formData = new FormData();
        for(var a in serializeArray)
            formData.append(serializeArray[a]["name"], serializeArray[a]['value']);
        formData.append("ufile", file, file.name);
        formData.set('csrf_token', core.csrf_token);

        if (setIdToZero) {
            formData.set('id', 0);
        }

        $.ajax({
            url :$uploadform.prop('action'),
            type: 'POST',
            headers: {
               'X-CSRF-TOKEN': core.csrf_token
            },
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(response) {
                var data = eval('[' + response.split('", [')[1].split(']);')[0] + ']');
                trigger(data);
            }
        }).done(function(){
            count++;
            if (count == tocount) {
                framework.unblockUI();
            }
        });
    }
};

FormController.include({
    init: function (parent, model, renderer, params) {
        var _super = this._super.apply(this, arguments);
        var self = this;
        $(document).on("refresh_attachment", function() {
            self.sidebar.updateEnv(self.sidebar.env);
        });
        return _super;
    }
});

FormRenderer.include({
    _updateView: function ($newContent) {
        var base = this._super.apply(this, arguments);
        if (this.mode == "readonly") {
            this._renderDnD();
            this._initAddScreenshot();
        }
        return base;
    },

    _renderDnD: function() {
       var self = this;
       var $form = self.$('.o_form_sheet_bg');
       self.$dnd = $('<div class="dnd dnd-hidden"><div class="dnd-box"><span>'+_t('Attachment(s)')+'</span></div></div>')
                    .prependTo($form);
       initDnd($form, self.$dnd, self._uploadFilesAttachments);
    },

    _uploadFilesAttachments: function(files) {
        var $uploadform = $('form.o_form_binary_form');
        if ($uploadform.length ) {
            uploadAttachment($uploadform, files, function(){
                $(document).trigger('refresh_attachment');
            });
        }
    },

    _initAddScreenshot: function() {
        var self = this;
        var cancel_fn = function(){
            $('#screenshot_modal').css('display', 'none');
            $('#screenshot_modal_bg').css('display', 'none');
        };
        if ($('screenshot_modal_bg').length===0){
            $('body').append('<div id="screenshot_modal_bg" class="modal-backdrop  in" style="display:none;"></div>');
        }
        if ($('screenshot_modal_bg').length===0){
            $('body').append(''+
            '<div id="screenshot_modal" style="display: none;" class="modal o_technical_modal in">'+
                '<div class="modal-dialog modal-lg">'+
                    '<div class="modal-content">'+
                        '<div class="modal-header">'+
                            '<button type="button" class="close" data-dismiss="modal" aria-hidden="true" id="screenshot_x">×</button>'+
                            '<h4 class="modal-title">'+_t('Upload Screenshot')+'<span class="o_subtitle text-muted small"></span></h4>'+
                        '</div> '+
                        '<div class="modal-body o_act_window"><div class="o_view_manager_content"><div><div class="o_form_view o_form_nosheet o_form_editable">'+
                            '<div class="o_group"><tr>'+
                                '<td class="o_td_label"><label class="o_form_label" for="screenshot_filename">'+_t('Filename')+'</label></td>'+
                                '<td style="width: 100%;"><input class="o_field_char o_field_widget o_input" name="screenshot_filename" type="text" placeholder="" id="screenshot_filename" required></td>'+
                            '</tr></div>'+
                        '</div></div></div></div>'+
                        '<div class="modal-footer"><div><footer>'+
                            '<button type="object" class="btn btn-sm btn-primary" id="screenshot_attachment"><span>'+_t('Upload to attachment(s)')+'</span></button>'+
                            '<button class="btn btn-sm btn-default" id="screenshot_cancel"><span>'+_t('Cancel')+'</span></button>'+
                        '</footer></div></div>'+
                    '</div> '+
                '</div>'+
            '</div> ');
            $('#screenshot_x').click(cancel_fn);
            $('#screenshot_cancel').click(cancel_fn);

        }
        var modal = $('#screenshot_modal');
        var model_bg = $('#screenshot_modal_bg');

        document.onpaste = function (event) {
          if (self.mode !== "readonly") return;
          if ($('.o_content').find('.o_form_view').length === 0 ) return;
          var items = (event.clipboardData  || event.originalEvent.clipboardData).items;
          var blob = null;
          for (var i = 0; i < items.length; i++) {
            if (items[i].type.indexOf("image") === 0) {
              blob = items[i].getAsFile();
            }
          }
          if (blob !== null) {
              var d = new Date();
              var nowMilliseconds = $.datepicker.formatDate('yy-mm-dd-', d) + d.getHours() + '-'+ d.getMinutes() + '-' + d.getSeconds() + '-' + d.getMilliseconds();
              $('#screenshot_filename').val('Screenshot_'+nowMilliseconds);
              model_bg.css('display','block');
              modal.css('display','block');
              $('#screenshot_attachment').unbind().click({blob: blob, cancel_fn: cancel_fn, self: self}, self.upload_screenshot_attachment);
          }
        }
    },

    upload_screenshot_attachment: function(event) {
        var name = $('#screenshot_filename').val();
        var blob = event.data.blob;
        var self = event.data.self;

        if (name.length !== 0){
            blob = new File([blob], name+'.png', {type: 'image/png'});;
        }
        self._uploadFilesAttachments([blob]);
        event.data.cancel_fn();
    }
});

Chatter.include({
    init: function (parent, record, mailFields, options) {
        var response = this._super.apply(this, arguments);
        var self = this;
        $(document).on("refresh_attachment_from_note", function(e, s, file) {
            self.composer.on_attachment_change_per_dnd(file);
            uploadAttachment(s.$('.o_chatter').find('form.o_form_binary_form'), [file], function(data){
                self.composer.on_attachment_loaded_per_dnd(data);
            }, true);
        });
        return response;
    },

    _openComposer: function(options) {
       this._super.apply(this, arguments);

       var self = this;
       var $form = self.$('.o_chat_composer');
       var label = '';
       if (options.is_log) {
            label = _t('Notice Attachment(s)');
       } else  {
            label = _t('Message Attachment(s)');
       }
       self.$dnd = $('<div class="dnd dnd-hidden"><div class="dnd-box"><span>'+label+'</span></div></div>')
                    .prependTo($form);
       initDnd($form, self.$dnd, self._uploadFiles);
    },

    _uploadFiles: function(files) {
        for(var i in files) {
            if (i === 'length' || i === 'item') return;
            $(document).trigger('refresh_attachment_from_note', [self, files[i]]);
        }
    }
});

Composer.BasicComposer.include({
    on_attachment_change_per_dnd: function(f) {
        var self = this,
            files = [f],
            attachments = self.get('attachment_ids');

        _.each(files, function(file){
            var attachment = _.findWhere(attachments, {name: file.name});
            // if the files already exits, delete the file before upload
            if(attachment){
                self.AttachmentDataSet.unlink([attachment.id]);
                attachments = _.without(attachments, attachment);
            }
        });

        this.$attachment_button.prop('disabled', true);
        var upload_attachments = _.map(files, function(file){
            return {
                'id': 0,
                'name': file.name,
                'filename': file.name,
                'url': '',
                'upload': true,
                'mimetype': '',
            };
        });
        attachments = attachments.concat(upload_attachments);
        this.set('attachment_ids', attachments);
    },

    on_attachment_loaded_per_dnd: function(files) {
        var self = this,
            attachments = this.get('attachment_ids');

        _.each(files, function(file){
            if(file.error || !file.id){
                this.do_warn(file.error);
                attachments = _.filter(attachments, function (attachment) { return !attachment.upload; });
            }else{
                var attachment = _.findWhere(attachments, {filename: file.filename, upload: true});
                if(attachment){
                    attachments = _.without(attachments, attachment);
                    attachments.push({
                        'id': file.id,
                        'name': file.name || file.filename,
                        'filename': file.filename,
                        'mimetype': file.mimetype,
                        'url': session.url('/web/content', {'id': file.id, download: true}),
                    });
                }
            }
        }.bind(this));
        this.set('attachment_ids', attachments);
        this.$attachment_button.prop('disabled', false);
    }
});

});