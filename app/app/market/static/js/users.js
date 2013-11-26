(function(){

	var UserRoute = Backbone.Router.extend({});
    var UsersView = window.ahr.market.MarketBaseView.extend({
	 	initialize : function(filters){
    	    var that = this;    
            this.filters = filters;            
            this.initTemplates(filters);           
            this.filters.search=$('#q').val();
            this.setpagecoutner(this.filters, window.ahr.app_urls.getusercount);
            this.filters.types=["resource", "offer", "request"];
            return this;
        },
    });

    window.ahr= window.ahr || {};
    window.ahr.users = window.ahr.users || {};
    window.ahr.users.initUsers = function(filters){
        window.ahr.users.default_filters = window.ahr.clone(filters);
        var users = new UserView(filters);
        var user_route = new UserRoute(market);
        Backbone.history.start();        
    };

})();