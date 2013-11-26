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
        
        setFilterType: function(ftype){
            $('.filter-type').removeClass('btn-success');
            $('.filter-type.'+ftype).addClass('btn-success');
        },
        
        resetMarket: function(){
            $('#marketitems').empty();                        
            window.location.hash="";
            this.setItems(0);     
            this.setpagecoutner(this.filters,window.ahr.app_urls.getmarketcount);
        },
                
        search: function(){
            this.filters.search = $('#q').val();
            this.resetMarket();        
        },
    
        showItem: function(ev){
            var id = ev.currentTarget.getAttribute('item_id');
            window.location = window.ahr.app_urls.viewitem+id;
        },
            
        itemTypesfilter: function(ev){
            this.updateTypefilter(this,ev);
            this.resetMarket();
        },
        
        tagsfilter: function(ev){
            this.updateTagsfilter(this,ev);
            this.setFilterType("custom");
            this.resetMarket();            
        },
            
        setItems: function(page){
            var that = this;
            var dfrd = that.getItems(0+(10*page),
                        10+(10*page),
                        this.filters,
                        window.ahr.app_urls.getmarketitemfromto);

            dfrd.done(function(data){
                $.each(data, function(item){
                    data[item].fields.pk = data[item].pk;
                    var item_html = that.item_tmp(data[item].fields);
                    $('#marketitems').append(item_html);
                });
            });
           
        },
            
        initialize : function(filters){
            var that = this;    
            this.default_filters = window.ahr.clone(filters);
            this.filters = filters;            
            this.initTemplates(filters);           
            this.filters.search=$('#q').val();
            this.setpagecoutner(this.filters, window.ahr.app_urls.getmarketcount);
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