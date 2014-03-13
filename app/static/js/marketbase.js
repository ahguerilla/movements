window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = window.ahr.BaseView.extend({
  el: '#market',
  loadingScrollElemets: false,
  currentItem: 0,
  allItemsLoaded: false,
  itemsPerCall: 15,
  requiresResetOnNewOfferRequest: false,
  cookieread: false,
  filterheightOpen: 0,
  filterheightClosed: 0,

  setFiltersDefault: function (tags) {
    this.filters[tags] = window.ahr.clone(this.default_filters[tags]);
  },

  setFilterNone: function (tags) {
    if (typeof tags == 'string') {
      this.filters[tags] = window.ahr.clone(this.default_filters[tags]);
    } else {
      this.filters = window.ahr.clone(this.default_filters);
    }
    var tagsarr = [];
    _.each(window.ahr[tags], function (item) {
      tagsarr.push(parseInt(item.pk, 10));
    });
    this.filters[tags] = tagsarr;
  },

  setFilterKeys: function (taghead) {
    var that = this;
    $('.row.' + taghead).empty();
    this.initFilters(that, taghead, that.tagtemp);

  },

  setFiltersFromCookie: function (that, items) {
    var cookie = $.cookie('tagfilters');
    if (typeof cookie != 'undefined') {
      if (items != "types") {
        that.filters[items] = cookie[items];
      }
    }
  },

  initFilters: function (that, items, templ) {
    _.each(window.ahr[items], function (item) {
      var activeFlag = ' ';
      if (_.contains(that.filters[items], item.pk)) {
        activeFlag = 'btn-success';
      }
      $('.row.btn-group-sm.' + items).append(templ({
        filtertag: item.value,
        active: activeFlag
      }));
    });
  },

  updateTagsfilter: function (that, ev) {
    a = $(ev.currentTarget.parentElement.parentElement).attr("item_title");
    ar = that.filters[a];
    data = window.ahr[a];
    var tagData = _.find(data, function (test) {
      return (test.value == ev.currentTarget.textContent);
    });
    if (tagData) {
      if (_.contains(ar, tagData.pk)) {
        that.filters[a] = _.filter(ar, function (item) {
          return item != tagData.pk;
        });
        $(ev.currentTarget).removeClass('btn-success');
      } else {
        that.filters[a].push(tagData.pk);
        $(ev.currentTarget).addClass('btn-success');
      }
    }
    $.cookie('tagfilters', that.filters);
  },

  updateTypefilter: function (that, ev) {
    that.filters.types.length = 0;
    var item_type = ev.currentTarget.getAttribute('item_type');
    if (that.types[item_type]) {
      that.filters.types.push(that.types[item_type]);
    }
  },

  setFilterType: function (tags, ftype) {
    $('input[name$="-' + tags + '"]').parent().removeClass('active');
    $('input[name="' + ftype + '-' + tags + '"]').parent().addClass('active');
  },

  search: function () {
    this.filters.search = $('#q').val();
    this.resetMarket();
  },

  filterKeySearch: function (ev) {
    ev.preventDefault();
    this.search();
    return false;
  },

  itemTypesfilter: function (ev) {
    this.updateTypefilter(this, ev);
    this.resetMarket();
  },

  tagsfilter: function (ev) {
    this.updateTagsfilter(this, ev);
    var tags = $(ev.currentTarget).closest('.btn-group-sm').attr('item_title');
    this.setFilterType(tags, 'cus');
    this.resetMarket();
  },

  initTemplates: function () {
    this.typetag_tmp = _.template($('#type-tag').html());
    this.tagtemp = _.template($('#filter-tag').html());
    for (var key in this.filters) {
      if (["skills", "countries", "issues"].indexOf(key) > -1) {
        this.initFilters(this, key, this.tagtemp);
      }
    }
    this.cookieread = true;
  },

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

  noSearchResult:function(){
    if($('.market-place-item').length==0){
        $('#marketitems').append('<p style="margin-top:20px;" id="no-search-result">Your search did not match any market item. <a href="#" id="searchagainall">Search again without any filters</a> or <a href="#" id="searchwithdefaults">search again with your default filters</a></p>');
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
          var item_html = that.item_tmp(item.fields);
          $itemhtml = $(item_html);
          var text = $itemhtml.find('.item-body').text();
          if(text.length>200){
            $itemhtml.find('.item-body').text(text.slice(0,200)+'...');
          }
          itemsToAppend.push($itemhtml[0].outerHTML);
          $('#marketitems').append($itemhtml[0].outerHTML);
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
      var self = this;
      this.offerdialog.oncomplete = function () {
        self.resetMarket();
      };
    }
  },

  getItems: function (from, to) {
    var that = this;
    that.filters.search = $('#q').val();
    return $.ajax({
      url: that.getitemfromto.replace('0', from) + to,
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: that.filters,
      traditional: true
    });
  },

  showItem: function (item_id) {
    var that = this;
    this.scroll = $(window).scrollTop();
    that.hideMarket();
    var dfrd = $.ajax({
      url: that.getItem + item_id
    });
    dfrd.done(function (item) {
      var html = that.item_tmp(item[0].fields);
      $('.comment-btn').data({
        id: item[0].pk
      });
      if ($(window).width() >= 992){
       $('.nanamorde').show();
      }else{
        $('.nanamorde-mobile').show();
      }

      $('#singleItem').html(html);
      $('#marketitem_comments').empty();
      that.item_widget.afterset();
      $.getJSON(window.ahr.app_urls.getcommentslast.replace('0', item_id) + '10000', function (data) {
        that.ShowComments(data);
      });
      $.getJSON(window.ahr.app_urls.getprofile+item[0].fields.owner[0],function(data){
        var tmpl = $('#message-profile').html();
        var prof = _.template(tmpl);
        $('.userprofile').html(prof(data));
        $('.rateit').rateit();
        $('.rateit').rateit('min', 0);
        $('.rateit').rateit('max', 5);
        $('.rateit').rateit('readonly', true);
        $('.rateit').each(function(){
          $(this).rateit('value', this.getAttribute('rate'));
        });
        var ac_tmp = _.template($('#useraction-template').html());
        var actions = ac_tmp({'username':data.username,
          'usercore':data.score,
          'ratecount':data.ratecount,
          'avatar': data.avatar
          });
        $('.action-container').html(actions);
        $('.actionitem.routehref',$('#singleItem')).empty();
    });
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

  showHideNanamorde: function(){
    if($('.nanamorde-mobile').css('display')!== 'none' && $(window).width() >= 992 ){
      $('.nanamorde').css('display','block');
      $('.nanamorde-mobile').css('display','none');
    }else if ($('.nanamorde').css('display') === 'block' && $(window).width() < 992 ){
      $('.nanamorde').css('display','none');
      $('.nanamorde-mobile').css('display','block');
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

  filterButtonHide: function (ev) {
    $('#filterbuttontext').html('&nbsp; Show Filters &nbsp;');
    $('#togglefilter').removeClass('dropup');
    $('#filterscroll').removeClass('filterscroll');
    this.setFilterWrapperMargin(this.filterheightClosed, 0);
  },

  filterButtonShow: function (ev) {
    $('#filterbuttontext').html('&nbsp; Hide Filters &nbsp;');
    $('#togglefilter').addClass('dropup');
    $('#filterscroll').addClass('filterscroll');
    this.setFilterWrapperMargin(this.filterheightOpen, 300);
  },

  setFilterOpenHeight: function () {
    $('#market-filters').removeClass('collapse');
    this.filterheightOpen = $('#fixed-filters').height();
    $('#market-filters').addClass('collapse');
  },

  bulkCustomizeFilters: function (tag, action) {
    if (action == 'all') {
      this.setFilterNone(tag);
    }
    if (action == 'def') {
      this.setFiltersDefault(tag);
    }
    if (action == 'cus') {
      this.setFiltersFromCookie(this, tag);
    }
    var tmp = $.cookie('bulkfilters');
    tmp[tag] = action;
    $.cookie('bulkfilters', tmp);
    this.setFilterKeys(tag);
    this.resetMarket();
  },

  bulkCustomizeFiltersEV: function (ev) {
    var val = $('input', $(ev.currentTarget)).attr('name').split('-');
    action = val[0];
    tag = val[1];
    this.bulkCustomizeFilters(tag, action);
  },

  initBulkFilters: function (bulksArg) {
    var bulks;
    if (typeof bulksArg === 'undefined'){
         bulks = $.cookie('bulkfilters');
    }else{
        bulks = bulksArg;
    }
    if (typeof bulks === "undefined") {
      bulks = {
        countries: "all",
        issues: "all",
        skills: "all"
      };
      $.cookie('bulkfilters', bulks);
      $('.filter-bulk-selector.all').addClass('active');
    }
    var that = this;
    _.each(bulks, function (selection, tag) {
      that.bulkCustomizeFilters(tag, selection);
      $('.filter-bulk-selector.' + selection + '-' + tag).addClass('active');
    });
  },

  setFilterWrapperMargin: function (height, speed) {
    $('#filter-wrapper').animate({
      height: height
    }, speed);
  },

  markAll:function(){
    $('.tagbutton', $('.row')).removeClass('btn-success');
    $('.tagbutton', $('.row')).addClass('btn-success');
    this.filters.types = _.values(this.types);
    this.filters.skills = _.keys(window.ahr.skills_lookup);
    this.filters.issues = _.keys(window.ahr.issues_lookup);
    this.filters.countries = _.keys(window.ahr.countries_lookup);
    $('.btn.filter-bulk-selector').removeClass('active');
    $('.btn.filter-bulk-selector.all').addClass('active');
  },

  searchWithNoFilters: function  (){
    this.markAll();
    this.resetMarket();
  },

  searchWithDefaultFilters:function(){
    $('.btn.filter-bulk-selector').removeClass('active');
    var bulks = {
        countries: "def",
        issues: "def",
        skills: "def"
      };
    this.initBulkFilters(bulks);
  },

  itemTagCick: function(ev) {
    var that = this;
    if(that.isSingle()===true)return;
    that.markAll();
    var tagType = ev.currentTarget.getAttribute('tagtype');
    var len = ev.currentTarget.textContent.length;
    var tag = ev.currentTarget.textContent.slice(1,len-1)
    data = window.ahr[tagType];
    var tagData = _.find(data, function (test) {
      return (test.value == tag);
    });
    $('.btn.filter-bulk-selector.'+tagType).removeClass('active');
    $('.tagbutton', $('.row.'+tagType)).removeClass('btn-success');
    $('.tagbutton', $('.row.'+tagType)).each(function(){
      if($(this).text()==tag){
        $(this).addClass('btn-success');
        return false;
      }
    });
    that.filters[tagType] = [tagData.pk];
    that.filters.types = _.values(that.types);
    that.resetMarket();
  },

  init: function (filters) {
    var that = this;
    $.cookie.json = true;
    $('.nanamorde').hide();
    this.filter_widget = window.widgets.filter_widget.initWidget('filter-container');
    $('#fixed-filters').affix({
      offset: {
        top: 300
      }
    });

    $.subscribe("nanamorde.resize", this.showHideNanamorde);
    $(window).resize(this.showHideNanamorde);

    $.subscribe("nanamorde.resize", this.showHideNanamorde);
    $(window).resize(this.showHideNanamorde);

    var resizeFilters = function() {
      that.setFilterOpenHeight();
      var newHight = $('#fixed-filters').height();
      $('#filter-wrapper').height(newHight + "px");
    };

    $.subscribe("filters.resize", resizeFilters);
    $(window).resize(resizeFilters);
    this.default_filters = window.ahr.clone(filters);
    this.requestdialog = window.ahr.request_form_dialog.initItem(false);
    this.offerdialog = window.ahr.offer_form_dialog.initItem(false);
    this.recommend_dialog = window.ahr.recommend_widget.initWidget(window.ahr.username);
    this.reportUserWidget = window.ahr.reportUserDialog.initWidget('body');
    $('#market-filters').on('show.bs.collapse', this.filterButtonShow.bind(this));
    $('#market-filters').on('hide.bs.collapse', this.filterButtonHide.bind(this));

    this.filters = filters;
    this.initTemplates(filters);
    this.filters.search = $('#q').val();
    this.events = _.extend(this.events, {
      'click .tagbutton': 'tagsfilter',
      'click #searchbtn': 'search',
      'click .item-type': 'itemTypesfilter',
      'click #create_offer': 'create_offer',
      'click #create_request': 'create_request',
      'click .filter-bulk-selector': 'bulkCustomizeFiltersEV',
      'click #searchagainall': 'searchWithNoFilters',
      'click #searchwithdefaults' : 'searchWithDefaultFilters',
      'submit': 'filterKeySearch',
      'click .btn.tag-button': 'itemTagCick'
    });

    // calculate height of the market-filters when opened and closed so we can set
    // the height of the market-filter correctly when we fix it to the top
    this.filterheightClosed = $('#filter-wrapper').height();
    this.setFilterOpenHeight();
    $('#filter-wrapper').height(this.filterheightClosed + "px");
    this.initBulkFilters();
  }

});