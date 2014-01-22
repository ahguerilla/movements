(function(){

    var UserRoute = Backbone.Router.extend({
        routes:{
            "": "page"
        },

        page: function(page){
            this.users.initInfiniteScroll();
        },

        initialize: function(users){
            this.users=users;
        }
    });

    var UsersView = window.ahr.market.MarketBaseView.extend({
        types:{"Activist" : "activist", "Ready to help" : "readytohelp" },

        recommend: function(ev){
            var username = $(ev.currentTarget).attr('username');
            window.ahr.recommend_widget.initWidget(username);
            $('#recsub').val($('#currentusername').text()+ ' recommends user '+ username);
            $('#recsub').attr('readonly',true);
            var href = '<a href="'+window.location.origin+'/uer/profile/'+username+'">'+username+'</a>';
            $('#recmessage').val($('#currentusername').text()+ ' recommends you have a look at '+ username + ' profile.' + ' \r\n'+ href );
            $('#touser').val('');
            $('#recommenddialog').modal('show');
        },

        Message: function(ev){
            var username = ev.currentTarget.getAttribute('username');
            this.message_widget.show(username,'','',false);
        },

        showItem: function(ev){
            window.location = $('a.linktoprofile',$(ev.currentTarget)).attr('href');
        },

        initialize : function(filters){
            var that = this;
            this.itemcount_url = window.ahr.app_urls.getusercount;
            this.getitemfromto = window.ahr.app_urls.getuserfromto;
            this.viewurl = window.ahr.app_urls.viewuserprofile;
            this.item_tmp = _.template($('#user-template').html());
            this.rate_widget = window.ahr.rate_form_dialog.initWidget('#'+this.el.id);
            this.message_widget = window.ahr.messagedialog_widget.initWidget('#'+this.el.id,'#infobar');
            this.item_widget = {afterset:function(){$.noop();}};

            filters.types=["activist", "readytohelp"];
            this.init(filters);
            window.ahr.expandTextarea('#newmessage');
            $('#q').typeahead({
               limit: 5,
               remote: window.ahr.app_urls['getusernames']+'?username='+$('#touser').val()
               }).on('typeahead:selected', function (e, d) {
                 that.search();
                 console.log(e.keydown);
            });

            this.delegateEvents(_.extend(this.events,{
                'click .recommend': 'recommend',
                'click .sendprivatemessageuser': 'Message',
                'click .item_container': 'showItem'
            }));
            return this;
        },
    });

    window.ahr= window.ahr || {};
    window.ahr.users = window.ahr.users || {};
    window.ahr.users.initUsers = function(filters){
        var users = new UsersView(filters);
        var user_route = new UserRoute(users);
        Backbone.history.start();
    };

})();