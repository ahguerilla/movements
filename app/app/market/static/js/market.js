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

        changeFilterType: function(ev){            
            var that = this;
            $('.filter-type').removeClass('btn-success');        
            $(ev.currentTarget).addClass('btn-success');
            if(ev.currentTarget.textContent=="Defaul"){
                this.filters = window.ahr.clone(window.ahr.market.default_filters);
            }else{
                this.filters = window.ahr.clone(window.ahr.market.default_filters);
            }
            for(key in this.filters){
                $('.row.'+key).empty();
                this.initFilters(that, key, that.tagtemp);
            }
            this.resetMarket();
        },

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
            that.filters = filters;
            this.typetag_tmp = _.template($('#type-tag').html());
            this.tagtemp = _.template($('#filter-tag').html());
            this.item_tmp = _.template($('#item_template').html());
            
            for(key in filters){
                that.initFilters(that, key, this.tagtemp);
            }
            this.initTypeTags(this.types, this.typetag_tmp);
            
            this.filters.search=$('#q').val();
            this.setpagecoutner(this.filters, window.ahr.app_urls.getmarketcount);
            this.filters.types=["resource", "offer", "request"];
            return this;
        },
    });

    window.ahr= window.ahr || {};
    window.ahr.market = window.ahr.market || {};
    window.ahr.market.initMarket = function(filters){
        window.ahr.market.default_filters = window.ahr.clone(filters);
        var market = new MarketView(filters);
        var market_route = new MarketRoute(market);
        Backbone.history.start();        
    };
})();