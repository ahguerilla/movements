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
        tagdict: {},
        events:{
            'click .sendprivatemessageuser': 'showpMessage',
            'click .sendpm': 'sendpm',
            'click .cancelpm': 'cancelpm',
            'click .btn.rate': 'showrate',
            'click .sendrate': 'setrate',
            'click .cancelrate': 'resetrate',
            'click #expdate-neverexpire': 'neverexp',
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
        },

        showrate: function(ev){
            this.evrate = ev;
            var username = ev.currentTarget.getAttribute('username');
            var image_src = ev.currentTarget.getAttribute('image_src');
            var score = ev.currentTarget.getAttribute('score');
            var ratecount = ev.currentTarget.getAttribute('ratecount');

            $('#ratecount').text(ratecount);
            if ($(ev.currentTarget).attr('rateing')=='user'){
                this.rateurl = window.ahr.app_urls.setuserrate+username;
                $('#username').text(username);
                $('#ratetitle').text(username);
            }else{

                this.rateurl = window.ahr.app_urls.marketsetrate+$("#item-single").attr("item-id");
                $('#username').text($('#marketitem_title').text());
                $('#ratetitle').text($('#marketitem_title').text());

            }
            $('#ratedialog').modal('show');

            $('#numstars').rateit();
            $('#numstars').rateit('min',0);
            $('#numstars').rateit('max',5);
            $('#numstars').rateit('readonly',true);
            $('#numstars').rateit('value',score);

            $('#profileimage').attr('src',image_src);

        },

        setrate: function(ev){
            var that = this;
            var event = ev;
            if($('input[name="stars"]:checked').val() == undefined){
                this.alert('You have to select a rateing.','#rateerror');
                return;
            }
            window.ahr.getcsrf(function(csrf){

                var dfrd = $.ajax({
                    url: that.rateurl,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        score:$('input[name="stars"]:checked').val(),
                        csrfmiddlewaretoken :csrf.csrfmiddlewaretoken,
                        }
                });
                dfrd.done(function(data){
                    $(that.evrate.currentTarget).attr('ratecount',data.ratecount);
                    $(that.evrate.currentTarget).attr('score',data.score);
                    $('#ratedialog').modal('hide');
                    that.resetrate();
                });
                dfrd.fail(function(data){
                    that.alert('Rating failed.','#rateerror');
                });
            });
        },

        resetrate: function(){
            $('input[name="stars"]:checked').prop('checked',false);
        }

    });
})();

