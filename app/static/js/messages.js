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
            //'click #reply-btn': 'reply'
        },

    reply: function(ev){
        ev.reventDefault()
    },

    openConv: function(ev){
        ev.preventDefault();

    var dfrd = $.ajax({
        url: ev.currentTarget.href,
        dataType: 'html'
    });

    dfrd.done(function(data){
        $('#conversation').html(data);
    });
    return false;
},

    initialize: function(){
        $.noop();
    }
    });

    window.ahr= window.ahr || {};
    window.ahr.messages = window.ahr.messages || {};
    window.ahr.messages.initInbox = function(){
    var messages = new InboxView();
    var messages_route = new InboxRoute(messages);
    $($('.conv_link')[0]).trigger('click');
    Backbone.history.start();
};
})();
