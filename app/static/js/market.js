(function () {
  var MarketFilterView = Backbone.View.extend({
    events: {
    }
  });

  var MarketView = window.ahr.market.MarketBaseView.extend({
    types: {
      "Offers": "offer",
      "Request": "request"
    },

    initialize: function (filters) {
      this.item_type = 'item';
      this.getitemfromto = window.ahr.app_urls.getmarketitemfromto;
      this.item_tmp = _.template($('#item_template').html());
      this.init(filters);
      _.extend(this.events,{'click .routehref': 'gotoItem'} );
      return this;
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.market = window.ahr.market || {};
  window.ahr.market.initMarket = function (filters) {
    var filterView = new MarketFilterView({el: ''});
    var market = new MarketView(filterView);
    market.initInfiniteScroll();
    document.title = window.ahr.string_constants.exchange;
  };
})();
