(function(){

    setInterval(function(){
        var text;
        $.getJSON(window.ahr.app_urls.getmessagecount,function(data){
            $('.message-counter').each(function(tmp,item){
                if(data>0){
                   $('#msgcntr',$(item)).text('('+data+')');
                }
            });
        });
    },30000);

    window.ahr= window.ahr || {};
    window.ahr.BaseView = Backbone.View.extend({
        events:{},
        showModalDialog: function(templateId, templateData, dialogId, callback) {
            var tmpl = _.template($(templateId).html());
            var tmpl_html = tmpl(templateData);
            $('#modal-placeholder').html(tmpl_html);
            $(dialogId).modal('show');
            if(callback){
                $(dialogId).on('shown.bs.modal', callback);
            }
        },

        invert: function (obj) {
            var new_obj = {};
            for (var prop in obj) {
                if(obj.hasOwnProperty(prop)) {
                    new_obj[obj[prop]] = prop;
                }
            }
            return new_obj;
        },

        alert: function(message,selector){
            $(selector).empty();
            $(selector).prepend('<div class="alert alert-warning alert-dismissable">'+
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
            message+'</div>');
        },

        info: function (message,selector){
            $(selector).empty();
            $(selector).prepend('<div class="alert alert-success alert-dismissable">'+
                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                message+'</div>');
        }
    });
})();
