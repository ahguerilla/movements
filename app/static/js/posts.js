(function(){
    var PosttRoute = Backbone.Router.extend({
        routes:{
            "": "page",
            "p:page": "page"
        },

        page: function(page){
            if(page){
                $('#marketitems').empty();
                this.posts.setItems(parseInt(page)-1);
            }else{
                this.posts.setItems(0);
            }
        },

        initialize: function(posts){
            this.posts=posts;
        }
    });

    var PostsView = window.ahr.market.MarketBaseView.extend({
        types:{"Resources":"resource","Offers":"offer","Request":"request"},

        deleteItem: function(ev){
            var that = this;
            if(confirm('Are you sure you want to delete this item?')){
                var item_id = ev.currentTarget.getAttribute('item_id');
                var dfrd = $.ajax({
                    url:window.ahr.app_urls.deletemarketitem+item_id,
                });
                dfrd.done(function(data){
                    that.alert('Item deleted','#infobar');
                    $(".row.item_container[item_id='"+ item_id + "']").remove();
                });
            }

            return(false);
        },

        showItem: function(ev){
            var that = this;
            var id = ev.currentTarget.getAttribute('item_id');
            $.getJSON(window.ahr.app_urls.getmarketitem+id,function(item){
                if(item[0].fields.item_type == "request"){
                    that.requestdialog.edit(item);
                    that.requestdialog.showModal();
                }else{
                    that.offerdialog.edit(item);
                    that.offerdialog.showModal();
                }
            });
        },


        initialize : function(filters){
            var that = this;
            this.item_tmp = _.template($('#item_template').html());
            this.itemcount_url = window.ahr.app_urls.getuseritemscount;
            this.getitemfromto = window.ahr.app_urls.getusermarketitemsfromto;
            this.viewurl = window.ahr.app_urls.edititem;
            filters.types=["resource", "offer", "request"];
            this.init(filters);
            this.delegateEvents(_.extend(this.events,{
                'click .delete-item': 'deleteItem',
            }));
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