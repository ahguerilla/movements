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
    
    
    var MarketView = Backbone.View.extend({        
        el: '#market',
        events:{
            'click .item_container': 'showItem',
            'click .tagbutton': 'filter',
            'click #searchbtn': 'search',            
            'keyup input[name="q"]': 'search',
            'click .item-type': 'typefilter'
        },
        types:{"Resources":"resource","Offers":"offer","Request":"request"},
                
        search: function(){
            this.filters.search = $('#q').val();
            $('#marketitems').empty();                        
            window.location.hash="";
            this.setItems(0);     
            this.setpagecoutner();
        },
    
        showItem: function(ev){
            var id = ev.currentTarget.getAttribute('item_id');
            window.location = window.app_urls.viewitem+id;
        },
    
        getItems: function(from,to,filts){
            filts.search=$('#q').val();
            return $.ajax({
                url:window.app_urls.getmarketitemfromto.replace('0',from)+to,
                dataType: 'json',
                contentType:"application/json; charset=utf-8",
                data: filts,
                traditional: true
            });
        },
        
        getItemsCount: function(filts){           
            return $.ajax({               
                url:window.app_urls.getmarketcount,
                dataType: 'json',
                contentType:"application/json; charset=utf-8",
                data: filts,
                traditional: true
            });
        },
        
        typefilter: function(ev){
            var ind = this.filters.types.indexOf(this.types[ev.currentTarget.textContent]);
            if(ind<0){
                this.filters.types.push(this.types[ev.currentTarget.textContent]);
                $(ev.currentTarget).addClass('btn-success');
            }else{
                this.filters.types.splice(ind,1);
                $(ev.currentTarget).removeClass('btn-success');
            }
            $('#marketitems').empty();                        
            window.location.hash="";
            this.setItems(0);
            this.setpagecoutner();
        },
        
        filter: function(ev){
            var that=this;
            a=$(ev.currentTarget.parentElement.parentElement).attr("item_title");
            ar = this.filters[a];
            inv = invert(window[a]);
            if (inv.hasOwnProperty(ev.currentTarget.textContent)){
                ind = inv[ev.currentTarget.textContent];
                filtind = ar.indexOf(parseInt(ind));
                if(filtind<0){
                    that.filters[a].push(parseInt(ind));
                    $(ev.currentTarget).addClass('btn-success');
                }else{
                    that.filters[a].splice(filtind,1);
                    $(ev.currentTarget).removeClass('btn-success');
                }
            }
            $('#marketitems').empty();                        
            window.location.hash="";
            this.setItems(0);
            this.setpagecoutner();
            
        },
        
        getfilter: function(){
            $.noop();
        },
        
        initFilters:function(items){       
            var that = this;        
            _.each(window[items],function(item,key){            
                if (that.filters[items].indexOf(parseInt(key))>-1){
                     $.noop();
                }else{
                    $('.row.btn-group-sm.'+items).append(that.tagtemp({filtertag:item, active:' '}));
                }
            }); 
        },
        
        setFilters: function(){
            var that = this;                
            for(item_ind in that.filters){
                var item = that.filters[item_ind];
                for(ind in item){
                    var i = item[ind];
                    $('.row.btn-group-sm.'+item_ind).append(that.tagtemp({filtertag:window[item_ind][i], active:'btn-success'}));
                }        
            }         
        },
        
        setItems: function(page){
            var that = this;
            var dfrd = this.getItems(0+(10*page),10+(10*page),this.filters);
            dfrd.done(function(data){
                $.each(data, function(item){
                    data[item].fields.pk = data[item].pk;
                    var item_html = that.item_tmp(data[item].fields);
                    $('#marketitems').append(item_html);
                });
            });
           
        },
        
        setpagecoutner:function(){
            $(".marketitems.pagination").empty();
            filters = this.filters;
            filters.search=$('#q').val();
            var cdfrd = this.getItemsCount(filters);
            cdfrd.done(function(data){
                var pages = Math.ceil(data.count/10);
                for(i=1;i<=pages;i++){
                    $(".marketitems.pagination").append("<li><a class='itempage' page='"+i+"' href='#p"+i+"'>"+i+"</a></li>");
                }
            });
        },
    
        initialize : function(filters){
            var that = this;                 
            this.tagtemp = _.template($('#filter-tag').html());
            this.item_tmp = _.template($('#item_template').html());
            that.filters = filters;            
            this.setFilters(filters);            
            for(item_ind in that.filters){
                that.initFilters(item_ind);
            }            
            this.setpagecoutner();
            this.filters.types=["resource","offer","request"];
            return this;
        },
    });

    window.market = window.market || {};
    window.market.initMarket = function(filters){
        window.ahr.default_filters = filters;
        var market = new MarketView(filters);
        var market_route = new MarketRoute(market);
        Backbone.history.start();        
    };
})();