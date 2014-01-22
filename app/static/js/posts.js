(function(){
    var PosttRoute = Backbone.Router.extend({
        routes:{
            "": "page",
            "item/:item_id": "gotoItem"
        },
        firstTime: true,
        emptyPage: true,

        gotoItem: function(item){
            this.market.showItem(item);
        },

        page: function(){
            if(this.firstTime){
                this.market.showMarket();
                this.market.initInfiniteScroll();
                this.market.scrollBack();

                this.firstTime = false;
            }else{
                this.market.resetSingle();
                this.market.showMarket();
                this.market.refreshScrollElements();
                this.market.scrollBack();
            }
        },

        initialize: function(market){
            this.market = market;
        }
    });

    var PostsView = window.ahr.market.MarketBaseView.extend({
        types:{"Offers":"offer","Request":"request"},

        initialize : function(filters){
            var that = this;
            this.item_tmp = _.template($('#item_template').html());
            this.itemcount_url = window.ahr.app_urls.getuseritemscount;
            this.getitemfromto = window.ahr.app_urls.getusermarketitemsfromto;
            this.viewurl = window.ahr.app_urls.edititem;
            this.requiresResetOnNewOfferRequest = true;
            filters.types=["offer", "request"];
            func = _.bind(this.del_callback, this);
            this.item_widget = window.ahr.marketitem_widget.initWidget('body',this,func);
            this.getItem = window.ahr.app_urls.getuseritem;
            this.init(filters);
            return this;
        },
});
    window.ahr= window.ahr || {};
    window.ahr.posts = window.ahr.posts|| {};
    window.ahr.posts.initPosts = function(filters){
        var posts = new PostsView(filters);
        var posts_route = new PosttRoute(posts);
        Backbone.history.start();
    };
})();