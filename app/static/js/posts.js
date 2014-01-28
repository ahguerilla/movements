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
        edit_callback:function(item_id){
            var that = this;
            var dfrd = $.ajax({url: this.getItem+item_id});
            dfrd.done(function(item){
                var html = that.item_widget.reloadItem(item);
                $('.market-place-item[item_id='+item_id+']').replaceWith(html);
                that.msnry.reloadItems();
                that.item_widget.afterset('.market-place-item[item_id='+item_id+']');
                if(that.isSingle()===false){
                   that.fancyref(html);
                }
            });
        },

        initialize : function(filters){
            var that = this;
            $('#backtothemarket').attr('href',window.ahr.app_urls.getposts+'/#');
            this.item_tmp = _.template($('#item_template').html());
            this.getitemfromto = window.ahr.app_urls.getusermarketitemsfromto;
            this.viewurl = window.ahr.app_urls.edititem;
            this.requiresResetOnNewOfferRequest = true;
            filters.types=["offer", "request"];
            var func = _.bind(this.del_callback, this);
            var edit_func = _.bind(this.edit_callback,this);
            this.item_widget = window.ahr.marketitem_widget.initWidget('body',this,func,edit_func);
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