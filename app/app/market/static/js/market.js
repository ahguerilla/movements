(function(){

    var MarketRoute = Backbone.Router.extend({
        routes:{
            "": "page",
            "p:page": "page"
        },
        
        page: function(page){
            if(page){
                $('#marketitems').empty();
                this.market.setItems(parseInt(page)-1);
            }else{
                this.market.setItems(0);
            }
        },
        
        initialize: function(market){
            this.market=market;            
        }
    });
    
    
    var MarketView = window.ahr.market.MarketBaseView.extend({                
        types:{"Resources":"resource","Offers":"offer","Request":"request"},
       
        showItem: function(ev){
            var id = ev.currentTarget.getAttribute('item_id');
            window.location = window.ahr.app_urls.viewitem+id;
        },
            
        initialize : function(filters){            
            this.itemcount_url = window.ahr.app_urls.getmarketcount;
            this.getitemfromto = window.ahr.app_urls.getmarketitemfromto
            this.item_tmp = _.template($('#item_template').html());           
            this.init(filters);
            this.filters.types=["resource", "offer", "request"];
            
            return this;
        },
    });

    window.ahr= window.ahr || {};
    window.ahr.market = window.ahr.market || {};
    window.ahr.market.initMarket = function(filters){        
        var market = new MarketView(filters);
        var market_route = new MarketRoute(market);
        Backbone.history.start();        
    };
})();