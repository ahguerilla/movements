(function () {
  var MarketRoute = Backbone.Router.extend({
    routes: {
      "": "page",
      "item/:item_id": "gotoItem"
    },
    firstTime: true,
    emptyPage: true,

    gotoItem: function (item) {
      this.market.showItem(item);
    },

    page: function () {
      if (this.firstTime) {
        this.market.showMarket();
        this.market.initInfiniteScroll();
        this.market.scrollBack();

        this.firstTime = false;
      } else {
        this.market.resetSingle();
        this.market.showMarket();
        this.market.refreshScrollElements();
        this.market.scrollBack();
      }
    },

    initialize: function (market) {
      this.market = market;
    }
  });

  var MarketView = window.ahr.market.MarketBaseView.extend({
    types: {
      "Offers": "offer",
      "Request": "request"
    },

    edit_callback: function (item_id) {
      var that = this;
      var dfrd = $.ajax({
        url: this.getItem + item_id
      });
      dfrd.done(function (item) {
        var html = that.item_widget.reloadItem(item);
        $('.market-place-item[item_id=' + item_id + ']').replaceWith(html);
        that.msnry.reloadItems();
        that.item_widget.afterset('.market-place-item[item_id=' + item_id + ']');
        if (that.isSingle() === false) {
          that.fancyref(html);
        }
      });
    },


    initialize: function (filters) {
      this.item_type = 'item';
      this.getitemfromto = window.ahr.app_urls.getmarketitemfromto;
      this.viewurl = window.ahr.app_urls.viewitem;
      this.item_tmp = _.template($('#item_template').html());
      this.requiresResetOnNewOfferRequest = true;
      del_func = _.bind(this.del_callback, this);
      edit_func = _.bind(this.edit_callback, this);
      this.item_widget = window.ahr.marketitem_widget.initWidget('body', this, del_func, edit_func);
      filters.types = ["offer", "request"];
      this.getItem = window.ahr.app_urls.getmarketitem;
      this.init(filters);
      return this;
    },
  });

  window.ahr = window.ahr || {};
  window.ahr.market = window.ahr.market || {};
  window.ahr.market.initMarket = function (filters) {
    var market = new MarketView(filters);
    var market_route = new MarketRoute(market);
    Backbone.history.start();
    document.title = "Exchange";
  };
})();