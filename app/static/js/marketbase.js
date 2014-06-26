window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = window.ahr.BaseView.extend({
  loadingPage: false,
  allItemsLoaded: false,
  loadedOnce: false,
  currentCall: null,
  noResultsString: "",
  is_featured: false,
  $itemContainer: null,

  clearMarketPage: function () {
    this.$itemContainer.empty();
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

        var hasItem = false;
        _.each(data, function (item) {
          if (item.page_count) {
            that.pageCount = item.page_count;
            that.pageActive = item.current_page;
            that.pageSize = item.page_size;
          } else {
            hasItem = true;
            item.fields.pk = item.pk;
            var item_html = that.item_tmp(item.fields);
            that.$itemContainer.append(item_html);
            $('.tm-tag').each(function(){
               var txt = $('span',$(this)).text();
               $('.tag-button:contains('+txt+')').css('background-color','#cccccc');
            });
          }
        });
        if (!hasItem) {
          that.allItemsLoaded = true;
          that.noSearchResult();
        }
        that.loadingPage = false;
      });
      return dfrd;
    }
  },

  noSearchResult: function () {
    if ($('.market-place-item').length === 0) {
      this.$itemContainer.append(this.noResultsString);
      $('#pagination').hide();
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
  }
});
