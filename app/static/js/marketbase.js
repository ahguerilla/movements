window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = window.ahr.BaseView.extend({
  loadingScrollElements: false,
  currentItem: 0,
  allItemsLoaded: false,
  itemsPerCall: 15,
  loadedOnce: false,
  currentCall: null,
  noResultsString: "",
  

  levelReached: function (pixelTestValue) {
    if (!this.loadedOnce) {
      this.loadedOnce = true;
      return true;
    }

    // is it low enough to add elements to bottom?
    var pageHeight = Math.max(document.body.scrollHeight ||
      document.body.offsetHeight);
    var viewportHeight = window.innerHeight ||
      document.documentElement.clientHeight ||
      document.body.clientHeight || 0;
    var scrollHeight = window.pageYOffset ||
      document.documentElement.scrollTop ||
      document.body.scrollTop || 0;
    // Trigger for scrolls within 30 pixels from page bottom
    return pageHeight - viewportHeight - scrollHeight < pixelTestValue;
  },

  initInfiniteScroll: function () {
    $('#marketitems').empty();
    if (this.currentCall) {
      this.currentCall.abort();
      this.currentCall = null;
    }
    this.allItemsLoaded = false;
    this.currentItem = 0;
    this.loadingScrollElements = false;
    this.loadedOnce = false;

    this.loadScrollElements();
    var that = this;
    $(window).scroll(function () {
      that.loadScrollElements();
    });
    // For ipad
    document.addEventListener('touchmove', function (e) {
      that.loadScrollElements();
    }, false);
  },

  noSearchResult: function () {
    if ($('.market-place-item').length === 0) {
      $('#marketitems').append(this.noResultsString);
    }
  },

  loadScrollElements: function () {
    var that = this;
    if (!that.loadingScrollElements && that.levelReached(30) && !that.allItemsLoaded) {
      that.loadingScrollElements = true;

      $('#ajaxloader').show();

      var dfrd = that.getItems(
        that.currentItem,
        that.currentItem + that.itemsPerCall
      );

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
          item.fields.pk = item.pk;
          var item_html = that.item_tmp(item.fields);
          $('#marketitems').append(item_html);
          $('.tm-tag').each(function(){
             var txt = $('span',$(this)).text();
             $('.tag-button:contains('+txt+')').css('background-color','#cccccc');
          });
        });

        that.currentItem = that.currentItem + that.itemsPerCall;
        that.loadingScrollElements = false;
      });
    }
  },

  getItems: function (from, to) {
    var data = {};
    if(this.filterView) {
      this.filterView.setFilter(data);
    }
    return $.ajax({
      url: this.getitemfromto.replace('0', from) + to,
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
    this.filterView.on('filter', function() {that.initInfiniteScroll();});
  }
});
