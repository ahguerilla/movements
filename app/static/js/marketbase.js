window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = window.ahr.BaseView.extend({
  el: '#market',
  loadingScrollElemets: false,
  currentItem: 0,
  allItemsLoaded: false,
  itemsPerCall: 15,
  requiresResetOnNewOfferRequest: false,
  loadedOnce: false,


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
    this.allItemsLoaded = false;
    this.currentItem = 0;

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
      $('#marketitems').append(['<p style="margin-top:20px;float:left;width:100%;text-align:center;" id="no-search-result">',
        window.ahr.string_constants.market_search_no_match_a,
        '<a href="#" id="searchagainall">',
        window.ahr.string_constants.market_search_no_match_b + '</a>' + window.ahr.string_constants.market_search_no_match_c,
        '<a href="#" id="searchwithdefaults">' ,
        window.ahr.string_constants.market_search_no_match_d,
        '</a></p>'].join(' '));
    }
  },

  truncateLongText:function(item_html, pk){
   $itemhtml = $(item_html);
   var text = $itemhtml.find('.item-body').text();
    if(text.length>200){
      $itemhtml.find('.item-body').html(text.slice(0,200)+' ...<div href="#item/'+pk+'"  class="routehref readmore_marketitem">Read more</div>');
    }
  },

  loadScrollElements: function () {
    var that = this;
    if (!that.loadingScrollElemets && that.levelReached(30) && !that.allItemsLoaded) {
      that.loadingScrollElemets = true;
      $('#ajaxloader').show();
      var dfrd = that.getItems(
        that.currentItem,
        that.currentItem + that.itemsPerCall
      );

      var itemsToAppend = [];
      dfrd.done(function (data) {
        $('#no-search-result').remove();
        $('#ajaxloader').hide();

        if (data.length === 0) {
          that.allItemsLoaded = true;
          that.noSearchResult();
        }

        _.each(data, function (item) {
          item.fields.pk = item.pk;
          var item_html = that.get(item.fields);
          that.truncateLongText(item_html, item.pk);
          itemsToAppend.push(item_html[0].outerHTML);
          $('#marketitems').append(item_html[0].outerHTML);
          $('.tm-tag').each(function(){
             var txt = $('span',$(this)).text();
             $('.tag-button:contains('+txt+')').css('background-color','#cccccc');
          });
        });

        that.currentItem = that.currentItem + that.itemsPerCall;
        that.loadingScrollElemets = false;
      });
    }
  },

  getItems: function (from, to) {
    var that = this;
    return $.ajax({
      url: that.getitemfromto.replace('0', from) + to,
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: {},
      traditional: true
    });
  },

  scrollBack: function () {
    $(window).scrollTop(this.scroll);
  },

  ShowComments: function (comments) {
    var that = this;
    _.each(comments, function (comment) {
      that.item_widget.addCommentToCommentList(comment);
    });
  },

  del_callback: function (item_id) {
    $(".item-wrap[item_id='" + item_id + "']").remove();
  },

  get: function(data){
     var itemHtml = this.item_tmp(data);
     return $(itemHtml);
   },

  init: function (filterView) {
  }
});