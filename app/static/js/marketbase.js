window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = window.ahr.BaseView.extend({
  el: '#market',
  loadingScrollElemets: false,
  currentItem: 0,
  allItemsLoaded: false,
  itemsPerCall: 15,
  requiresResetOnNewOfferRequest: false,


  levelReached: function (pixelTestValue) {
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

  initInfiniteScroll: function (callback) {
    $('#marketitems').empty();
    this.allItemsLoaded = false;
    this.currentItem = 0;

    var $container = $('#marketitems');
    $container.masonry({
      itemSelector: '.market-place-item'
    });

    this.loadScrollElements(this, callback);
    var that = this;
    $(window).scroll(function () {
      that.loadScrollElements(that);

    });
    // For ipad
    document.addEventListener('touchmove', function (e) {
      that.loadScrollElements(that);
    }, false);
  },

  noSearchResult: function () {
    if ($('.market-place-item').length == 0) {
      $('#marketitems').append(['<p style="margin-top:20px;" id="no-search-result">',
        gettext('Your search did not match any market item.'),
        '<a href="#" id="searchagainall">',
        gettext('Search again without any filters')+'</a>'+gettext('or'),
        '<a href="#" id="searchwithdefaults">' ,
        gettext('search again with your default filters'),
        '</a></p>'].join(' '));
    }
  },

  loadScrollElements: function (self, callback) {
    var that = self;
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
        if (data.length === 0) {
          that.allItemsLoaded = true;
          $('#ajaxloader').hide();
          that.noSearchResult();
        }
        _.each(data, function (item) {
          item.fields.pk = item.pk;
          var item_html = that.get(_.extend(item.fields,{'isSingle': false}));
          $itemhtml = $(item_html);
          var text = $itemhtml.find('.item-body').text();
          if(text.length>200){
            $itemhtml.find('.item-body').text(text.slice(0,200)+'...');
          }
          itemsToAppend.push(item_html[0].outerHTML);
          $('#marketitems').append(item_html[0].outerHTML);
        });

        if (itemsToAppend.length > 0) {
          var container = document.querySelector('#marketitems');
          that.msnry = new Masonry(container);
          _.each(itemsToAppend, function (elem) {
            that.msnry.appended(elem);
          });

          that.item_widget.afterset();
          that.msnry.layout();
          $('#ajaxloader').hide();
        }

        that.currentItem = that.currentItem + that.itemsPerCall;
        that.loadingScrollElemets = false;
        if (callback) {
          callback();
          return;
        }
      });
    }
  },

  fancyref: function () {
    this.msnry.layout();
  },

  resetMarket: function () {
    var that = this;
    var updateMarketScrollPosition = $('#fixed-filters').hasClass('affix');
    if (updateMarketScrollPosition) {
      $(".exchange-banner").hide();
    }
    this.initInfiniteScroll(function () {
      if (updateMarketScrollPosition) {
        var heightOfBanner = $('.exchange-banner').height();
        that.setScrollPostion(heightOfBanner + 2);
      } else {
        that.setScrollPostion(0);
      }
    });
  },

  setScrollPostion: function (height) {
    $(window).scrollTop(height);
  },

  create_request: function () {
    this.requestdialog.showModal(true);
    if (this.requiresResetOnNewOfferRequest && !this.requestdialog.oncomplete) {
      var self = this;
      this.requestdialog.oncomplete = function () {
        self.resetMarket();
      };
    }
  },

  create_offer: function () {
    this.offerdialog.showModal(true);
    if (this.requiresResetOnNewOfferRequest && !this.offerdialog.oncomplete) {
      var self = this; this.events = _.extend(this.events, {
        'click .tagbutton': 'tagsfilter',
        'click .item-type': 'itemTypesfilter',
        'click .filter-bulk-selector': 'bulkCustomizeFiltersEV',
        'click .btn.tag-button': 'itemTagCick'
      });
      this.offerdialog.oncomplete = function () {
        self.resetMarket();
      };
    }
  },

  getItems: function (from, to) {
    var that = this;
    that.filter_widget.filters.search = $('#q').val();
    return $.ajax({
      url: that.getitemfromto.replace('0', from) + to,
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: that.filter_widget.filters,
      traditional: true
    });
  },

  showItem: function (item_id) {
    var that = this;
    $('#singleItem').hide();
    this.scroll = $(window).scrollTop();
    that.hideMarket();
    var dfrd = $.ajax({url: that.getItem + item_id});
    dfrd.done(function (item) {
      var html = that.get(_.extend(item[0].fields,{'isSingle': true}));
      $('.comment-btn').data({id: item[0].pk});
      if ($(window).width() >= 992) {
        $('.nanamorde').show();
      } else {
        $('.nanamorde-mobile').show();
      }

      $('#singleItem').html(html);
      $('#marketitem_comments').empty();
      that.item_widget.afterset();

      $.getJSON(window.ahr.app_urls.getcommentslast.replace('0', item_id) + '10000',
        function (data) {
          that.ShowComments(data);
      });
      that.profile_widget.set(item[0].fields.owner[0],'.userprofile', 'user');
      $('#singleItem').show();
    });
  },

  refreshScrollElements: function () {
    this.msnry.destroy();
    var container = document.querySelector('#marketitems');
    this.msnry = new Masonry(container);
    this.msnry.layout();
  },

  resetSingle: function () {
    $('#singleItem').empty();
  },

  hideMarket: function () {
    $('.exchange-banner').hide();
    $('#backtothemarket').css('visibility', 'visible');
    $('#marketitem_comment_form').show();
    $('#marketitem_comments').show();
    $('#market-filters').collapse({
      toggle: false
    });
    $('#market-filters').collapse('hide');
    $('#togglefilter').hide();
    $('#itemandsearchwrap').hide();
    $.publish('filters.resize');
  },

  showMarket: function () {
    $('.exchange-banner').show();
    $('#backtothemarket').css('visibility', 'hidden');
    $('#itemandsearchwrap').show();
    $('#marketitem_comment_form').hide();
    $('#marketitem_comments').hide();
    $('#marketitem_comments').empty();
    $('#singleItem').empty();
    $('#togglefilter').show();
    $('#newcomment').val('');
    $('.nanamorde').hide();
    $('.nanamorde-mobile').hide();
    $.publish('filters.resize');

  },

  showHideNanamorde: function () {
    if ($('.nanamorde-mobile').css('display') !== 'none' && $(window).width() >= 992) {
      $('.nanamorde').css('display', 'block');
      $('.nanamorde-mobile').css('display', 'none');
    } else if ($('.nanamorde').css('display') === 'block' && $(window).width() < 992) {
      $('.nanamorde').css('display', 'none');
      $('.nanamorde-mobile').css('display', 'block');
    }
  },

  isSingle: function () {
    if ($('#marketitem_comments').is(":visible")) {
      return (true);
    }
    return (false);
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
    if (this.isSingle()) {
      window.location.hash = "";
    }
    $(".item-wrap[item_id='" + item_id + "']").remove();
    this.refreshScrollElements();
  },

  searchWithNoFilters: function () {
    this.filter_widget.markAll();
    this.resetMarket();
  },

  searchWithDefaultFilters: function () {
    var bulks = {
      countries: "def",
      issues: "def",
      skills: "def"
    };
    this.filter_widget.initBulkFilters(bulks);
  },

  get: function(data){
     var actionsHtml = this.actions_view.get(this.item_type, data);
     var itemHtml = this.item_tmp(data);
     var $itemHtml = $(itemHtml);
     $itemHtml.find('.action-place').replaceWith(actionsHtml);
     return  $itemHtml;
   },

  init: function (filters) {
    var that = this;
    this.actions_view = window.ahr.actions_view();
    $.subscribe("nanamorde.resize", this.showHideNanamorde);
    $(window).resize(this.showHideNanamorde);
    $.subscribe("nanamorde.resize", this.showHideNanamorde);
    $(window).resize(this.showHideNanamorde);

    this.filter_widget = window.widgets.filter_widget.initWidget(
      'filter-container',
      '#market',
      filters,
      window.ahr.clone(filters),
      this.resetMarket.bind(this),
      this.isSingle.bind(this)
      );
    this.filter_widget.initBulkFilters();
    this.profile_widget = window.ahr.profile_widget.initWidget(this.actions_view, window.ahr.app_urls.getprofile);
    this.requestdialog = window.ahr.request_form_dialog.initItem(false);
    this.offerdialog = window.ahr.offer_form_dialog.initItem(false);
    this.recommend_dialog = window.ahr.recommend_widget.initWidget(window.ahr.username);
    this.reportUserWidget = window.ahr.reportUserDialog.initWidget('body');

    _.extend(this.events, {
      'click #create_offer': 'create_offer',
      'click #create_request': 'create_request',
      'click #searchagainall': 'searchWithNoFilters',
      'click #searchwithdefaults': 'searchWithDefaultFilters',
    });


  }

});