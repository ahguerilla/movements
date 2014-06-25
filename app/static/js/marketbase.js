window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = window.ahr.BaseView.extend({
  loadingPage: false,
  allItemsLoaded: false,
  loadedOnce: false,
  currentCall: null,
  noResultsString: "",

//  levelReached: function (pixelTestValue) {
//    if (!this.loadedOnce) {
//      this.loadedOnce = true;
//      return true;
//    }
//
//    // is it low enough to add elements to bottom?
//    var pageHeight = Math.max(document.body.scrollHeight ||
//      document.body.offsetHeight);
//    var viewportHeight = window.innerHeight ||
//      document.documentElement.clientHeight ||
//      document.body.clientHeight || 0;
//    var scrollHeight = window.pageYOffset ||
//      document.documentElement.scrollTop ||
//      document.body.scrollTop || 0;
//    // Trigger for scrolls within 30 pixels from page bottom
//    return pageHeight - viewportHeight - scrollHeight < pixelTestValue;
//  },

  clearMarketPage: function () {
    $('#marketitems').empty();
    if (this.currentCall) {
      this.currentCall.abort();
      this.currentCall = null;
    }
    this.allItemsLoaded = false;
    this.loadingPage = false;
  },

  loadPage: function (page) {
    var that = this;
    if (!that.loadingPage && !that.allItemsLoaded) {
      that.loadingPage = true;

      this.clearMarketPage();
      $('#ajaxloader').show();

      var dfrd = that.getItems(page);

      this.currentCall = dfrd;

      dfrd.done(function (data) {
        this.currentCall = null;
        $('#no-search-result').remove();
        $('#ajaxloader').hide();

        if (data.length === 0) {
          that.allItemsLoaded = true;
          that.noSearchResult();
        }

        _.each(data, function (item) {
          if (item.page_count) {
            that.pageCount = item.page_count;
            that.pageActive = item.current_page;
            that.pageSize = item.page_size;
          } else {
           item.fields.pk = item.pk;
            var item_html = that.item_tmp(item.fields);
            $('#marketitems').append(item_html);
            $('.tm-tag').each(function(){
               var txt = $('span',$(this)).text();
               $('.tag-button:contains('+txt+')').css('background-color','#cccccc');
            });
          }
        });
        that.loadingPage = false;
      });
      return dfrd;
    }
  },

  noSearchResult: function () {
    if ($('.market-place-item').length === 0) {
      $('#marketitems').append(this.noResultsString);
    }
  },

  getItems: function (page) {
    var data = {};
    if(this.filterView) {
      this.filterView.setFilter(data);
    }
    data.page = page;
    return $.ajax({
      url: this.getMarketItems,
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: data,
      traditional: true
    });
  },

  scrollBack: function () {
    $(window).scrollTop(this.scroll);
  },

  init: function (filterView) {
    var that = this;
    this.filterView = filterView;
    //this.filterView.on('filter', function() {that.initMarket();});
  }
});
