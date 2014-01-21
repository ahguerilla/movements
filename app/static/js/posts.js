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

        showItem: function(item_id){
            var that = this;
            this.scroll = $(window).scrollTop();
            that.hideMarket();
            var dfrd = $.ajax({url:window.ahr.app_urls.getmarketitem+item_id});
            dfrd.done(function(item){
                var html = that.item_tmp(item[0].fields);
                $('.comment-btn').data({id:item[0].pk});
                $('#singleItem').append(html);
                that.item_widget.afterset();
                $.getJSON(window.ahr.app_urls.getcommentslast.replace('0',item_id)+'100',function(data){
                    that.ShowComments(data);
                });

            });
        },

        resetSingle: function(){
            $('#singleItem').empty();
        },

        hideMarket:function(){
            $('#itemandsearchwrap').hide();
            $('#marketitem_comment_form').show();
            $('#marketitem_comments').show();
            $('#market-filters').collapse({toggle:false});
            $('#market-filters').collapse('hide');
            $('#togglefilter').hide();
        },

        showMarket:function(){
            $('#singleItem').empty();
            $('#itemandsearchwrap').show();
            $('#marketitem_comment_form').hide();
            $('#marketitem_comments').hide();
            $('#marketitem_comments').empty();
            $('#newcomment').val('');
            $('#togglefilter').show();
        },

        scrollBack:function(){
            $(window).scrollTop(this.scroll);
        },

        ShowComments: function(comments){
            var that = this;
            _.each(comments, function(comment){
                that.item_widget.addCommentToCommentList(comment);
            });
        },

        initialize : function(filters){
            var that = this;
            this.item_tmp = _.template($('#item_template').html());
            this.itemcount_url = window.ahr.app_urls.getuseritemscount;
            this.getitemfromto = window.ahr.app_urls.getusermarketitemsfromto;
            this.viewurl = window.ahr.app_urls.edititem;
            this.requiresResetOnNewOfferRequest = true;
            filters.types=["offer", "request"];
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