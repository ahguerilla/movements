(function(){
    var MarketView = Backbone.View.extend({        
        el: '#market',        
        events:{
            'click .item_container': 'showItem',
            'click #searchbtn': 'search',
            'click .tagbutton': 'filter'
        },
        

    search: function(){
        window.getcsrf(function(csrf){                
            var data= {
                q:$('#q').val(),
                csrfmiddlewaretoken:csrf.csrfmiddlewaretoken,
            };
            window.location = 'search?'+$.param(data);
        });            
    },

    showItem: function(ev){
        var id = ev.currentTarget.getAttribute('item_id');
        window.location = window.app_urls.viewitem+id;
    },

    getItems: function(from,to,filts){           
        return $.ajax({
            url:window.app_urls.getmarketitemfromto.replace('0',from)+to,
            dataType: 'json',
            contentType:"application/json; charset=utf-8",
            data: filts,
            traditional: true
        });
    },
    
    filter: function(ev){
        $.noop();
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

    initialize : function(filters){
        var that = this;     
        this.tagtemp = _.template($('#filter-tag').html());
        this.item_tmp = _.template($('#item_template').html());
        that.filters = filters;
        this.setFilters(filters);
        for(item_ind in that.filters){
            that.initFilters(item_ind);
        }
        var dfrd = this.getItems(0,100,filters);
        dfrd.done(function(data){
            $.each(data, function(item){
                data[item].fields.pk = data[item]. pk;
                var item_html = that.item_tmp(data[item].fields);
                $('#marketitems').append(item_html);
            });
        });
    },
    });

    window.market = window.market || {};
    window.market.initMarket = function(filters){
        window.default_filters = filters;
        var market = new MarketView(filters);
    };
})();