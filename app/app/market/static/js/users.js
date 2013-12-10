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
        initialize : function(filters){
            this.itemcount_url = window.ahr.app_urls.getusercount;
            this.getitemfromto = window.ahr.app_urls.getuserfromto;
            this.viewurl = window.ahr.app_urls.viewuserprofile;
            this.item_tmp = _.template($('#user-template').html());
            filters.types=["activist", "readytohelp"];
            this.init(filters);
            window.ahr.expandTextarea('#newmessage');
            //this.delegateEvents(_.extend(this.events,{}));
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