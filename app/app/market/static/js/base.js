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
        events:{
            'click .sendprivatemessageuser': 'showpMessage',
            'click .sendpm': 'sendpm',
            'click .cancelpm': 'cancelpm',
            'click .btn.rate': 'showrate',
            'click .sendrate': 'setrate',
            'click .cancelrate': 'resetrate',
        },

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
        },

        sendpm: function(ev){
            var that = this;
            if( $('#msgsub').val()!== '' &&  $('#newmessage').val() !== ''){
                $('#messagedialog').modal('hide');
                window.ahr.getcsrf(function(csrf){
                    var dfrd = $.ajax({
                        url:window.ahr.app_urls.sendmessage+$('#usernameh').text(),
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            csrfmiddlewaretoken :csrf.csrfmiddlewaretoken,
                            subject: $('#msgsub').val(),
                            message: $('#newmessage').val()
                        }
                    });
                    dfrd.done(function(){
                        $('#market').prepend('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>Your message was sent successfuly.</div>');
                    });
                });
            }else{
                this.alert('Please provide a subject and message.','#pmerror');
            }
        },

        cancelpm: function(ev){
        },

        showpMessage: function(ev){
            var username = ev.currentTarget.getAttribute('username');
            $('#usernameh').text(username);
            $('#msgsub').val('');
            $('#newmessage').val('');
            $('#messagedialog').modal('show');
        }

    });
})();

