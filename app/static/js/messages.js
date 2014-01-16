(function(){
    var InboxRoute = Backbone.Router.extend({
        routes:{
            "": "page",
            "p:page": "page"
        },
        page: function(page){
            $.noop();
        },
        initialize: function(market){
            $.noop();
        }
    });

    var InboxView = Backbone.View.extend({
        el: '#pm_messages',
        events:{
            'click .conv_link': 'openConv',
            'click #back': 'back'
        },

        reply: function(ev){
            ev.reventDefault()
        },

        openConv: function(ev){
            var that = this;
            ev.preventDefault();
            if(ev.currentTarget.parentElement.tagName=="STRONG"){
                a = ev.currentTarget;
                $(ev.currentTarget.parentElement.parentElement).html(a);
            }

            var dfrd = $.ajax({
                url: ev.currentTarget.href,
                dataType: 'html'
            });

            dfrd.done(function(data){
               $('#conversation').html(data);
               that.showconv();
               $.getJSON(window.ahr.app_urls.getmessagecount,function(data){
                    $('.message-counter').each(function(tmp,item){
                        if(data>0){
                            $('#msgcntr',$(item)).text('('+data+')');
                        }else{
                            $('#msgcntr',$(item)).text('');
                        }
                    });
                });
            });
            return false;
        },

        showconv:function(){
            if($(window).width()<992){
                $("#message-col").hide();
                $('#conversation').show();
                $('#conversation')[0].scrollIntoView(true);

            }else{
                $.noop();
            }
        },

        back:function(ev){
            $('#conversation').hide();
            $("#message-col").show();
        },

        resize:function(ev){
            if($(window).width()<992){
                $('#conversation').hide();
            }else{
                $('#conversation').show();
                $("#message-col").show();
            }

        },

        initialize: function(){
            $(window).resize(this.resize);
            $.noop();
        }
    });

    window.ahr= window.ahr || {};
    window.ahr.messages = window.ahr.messages || {};
    window.ahr.messages.initInbox = function(){
    var messages = new InboxView();
    var messages_route = new InboxRoute(messages);
    if($(window).width()>992){
        $($('.conv_link')[0]).trigger('click');
    }

    Backbone.history.start();
};
})();
