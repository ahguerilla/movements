(function(){

	var UserRoute = Backbone.Router.extend({});
    var UsersView = window.ahr.market.MarketBaseView.extend({
    	
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