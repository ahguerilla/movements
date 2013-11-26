(function(){

	var UserRoute = Backbone.Router.extend({});
    var UsersView = window.ahr.market.MarketBaseView.extend({
	 	types:{"Activist" : "activist", "Ready to help" : "readytohelp" },
       
        showItem: function(ev){
            var id = ev.currentTarget.getAttribute('item_id');
            window.location = window.ahr.app_urls.viewitem+id;
        },
            
        initialize : function(filters){            
            this.itemcount_url = window.ahr.app_urls.getusercount;
            this.getitemfromto = window.ahr.app_urls.getuserfromto
            this.item_tmp = _.template($('#item_template').html());           
            this.init(filters);
            this.filters.types=["activist", "readytohelp"];            
            return this;
        },
    });

    window.ahr= window.ahr || {};
    window.ahr.users = window.ahr.users || {};
    window.ahr.users.initUsers = function(filters){       
        var users = new UsersView(filters);
        var user_route = new UserRoute(market);
        Backbone.history.start();        
    };

})();