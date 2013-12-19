(function(){

    var UserRoute = Backbone.Router.extend({
        routes:{
            "": "page",
            "p:page": "page"
        },

        page: function(page){
            if(page){
                $('#marketitems').empty();
                this.users.setItems(parseInt(page, 10)-1);
            }else{
                this.users.setItems(0);
            }
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
            $('#recsub').val($('#currentusername').text()+ ' recommeds user '+ username);
            $('#recsub').attr('readonly',true);
            var href = '<a href="'+window.location.origin+'/uer/profile/'+username+'">'+username+'</a>';
            $('#recmessage').val($('#currentusername').text()+ ' recommends you have a look at '+ username + ' profile.' + ' \r\n'+ href );
            $('#touser').val('');
            $('#recommenddialog').modal('show');
        },

        search: function(){
            this.filters.search = $('#q').val();
            this.resetMarket();
        },

        initialize : function(filters){
            this.itemcount_url = window.ahr.app_urls.getusercount;
            this.getitemfromto = window.ahr.app_urls.getuserfromto;
            this.viewurl = window.ahr.app_urls.viewuserprofile;
            this.item_tmp = _.template($('#user-template').html());
            filters.types=["activist", "readytohelp"];
            this.init(filters);
            window.ahr.expandTextarea('#newmessage');
            this.delegateEvents(_.extend(this.events,{
                'click .recommend': 'recommend',
                'click #searchbtn': 'search'
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