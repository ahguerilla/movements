(function(){
    var MarketView = Backbone.View.extend({
        el: '#market',
        events:{
            'click .item_container': 'showItem'
        },

        showItem: function(ev){
            var id = ev.currentTarget.getAttribute('item_id');
            window.location = window.app_urls.viewitem+id;
        },

        getItems: function(from,to){
            return $.ajax({
                url:window.app_urls.getmarketitemfromto.replace('0',from)+to,
                dataType: 'json'
            });
        },

        initialize : function(obj_id){
            var that = this;
            this.item_tmp = _.template($('#item_template').html());

            var dfrd = this.getItems(0,10);
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
    window.market.initMarket = function(){
        var market = new MarketView();
    };
})();