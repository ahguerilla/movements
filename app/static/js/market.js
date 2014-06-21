(function () {
  var MarketFilterView = Backbone.View.extend({
    type: '',
    regions: [],
    skills: [],
    showHidden: false,

    events: {
      'click .type-menu a': 'setTypeFilter',
      'click .hidden-menu a': 'setHiddenFilter',
      'click .region-filter a': 'setRegionFilter',
      'click .skill-filter a': 'setSkillsFilter'
    },

    initialize: function() {
      var $skills = this.$el.find('a.skills');
      var $container = $skills.parent().find('.popover-container');
      $skills.popover({
        title: '',
        html: true,
        content: _.template($('#skill-filter-list-template').html())(),
        container: $container,
        placement: 'bottom'
      });

      var $regions = this.$el.find('a.regions');
      $container = $regions.parent().find('.popover-container');
      $regions.popover({
        title: '',
        html: true,
        content: _.template($('#region-filter-list-template').html())(),
        container: $container,
        placement: 'bottom'
      });
    },

    toggleFilterState: function(ev) {
      ev.preventDefault();
      var $target = $(ev.currentTarget);
      $target.toggleClass('selected');
      return {
        id: $target.data('id'),
        selected: $target.hasClass('selected')
      };
    },

    setSkillsFilter: function (ev) {
      this.toggleFilterState(ev);
      this.trigger('filter');
    },

    setRegionFilter: function(ev) {
      this.toggleFilterState(ev);
      this.trigger('filter');
    },

    setHiddenFilter: function(ev) {
      ev.preventDefault();
      this.$el.find('.hidden-menu li.active').removeClass('active');
      var $filterLink = $(ev.currentTarget);
      $filterLink.parents('li').addClass('active');
      this.showHidden = $filterLink.data('filter');
      this.trigger('filter');
    },

    setTypeFilter: function(ev) {
      ev.preventDefault();
      this.$el.find('.type-menu li.active').removeClass('active');
      var $filterLink = $(ev.currentTarget);
      $filterLink.parents('li').addClass('active');
      this.type = $filterLink.data('filter');
      this.trigger('filter');
    },

    setFilter: function(data) {
      if (this.type) {
        data.types = this.type;
      }
      data.showHidden = this.showHidden;
    }
  });

  var MarketView = window.ahr.market.MarketBaseView.extend({
    types: {
      "Offers": "offer",
      "Request": "request"
    },

    events: {
      'click .market-place-item .item-menu': 'showMenuItem',
      'click .item-action-menu a': 'itemAction'
    },

    initialize: function (options) {
      this.item_type = 'item';
      this.getitemfromto = options.marketUrl;
      this.noResultsString = options.noResultsString;
      this.item_tmp = _.template($('#item_template').html());
      if(options.filterView) {
        this.init(options.filterView);
      }
      this.item_menu_template = _.template($('#item-menu-template').html());
      this.closeDialog = new ahr.CloseItemDialogView();
      this.reportDialog = new ahr.ReportPostView();
      return this;
    },

    createItemPopover: function($link) {
      var $container = $link.parent();
      var $itemContainer = $link.parents('.market-place-item');
      var toggled = {
        hide: $itemContainer.data('hidden'),
        stick: $itemContainer.data('stick')
      };
      var content = this.item_menu_template({
        hasEdit: $itemContainer.data('has-edit'),
        toggled: toggled
      });
      $link.popover({
        title: '',
        html: true,
        content: content,
        container: $container,
        placement: 'bottom'
      });
      $link.popover('show');
      $link.data('popover-made', true);
    },

    showMenuItem: function(ev) {
      var $link = $(ev.currentTarget);
      if ($link.data('popover-made')) {
        return;
      } else {
        ev.preventDefault();
        this.createItemPopover($link);
      }
    },

    setItemAttibute: function($container, attribute, value) {
      var data = {};
      data[attribute] = value;
      $.ajax({
        url: $container.data('attributes-url'),
        method: 'POST',
        context: this,
        data: data,
        success: this.initInfiniteScroll
      });
      $container.data(attribute, value);
    },

    itemAction: function(ev) {
      ev.preventDefault();
      var $link = $(ev.currentTarget);
      var action = $link.data('action');
      var $container = $link.parents('.market-place-item');
      var pk = $container.data('item-id');
      var itemType = $container.data('item-type');
      var that = this;
      var refresh = function () {
        that.initInfiniteScroll();
      }

      var remakePopover = false
      if (action === 'close') {
        var closeUrl = $container.data('close-url');
        this.closeDialog.close(pk, itemType, closeUrl, refresh);
      } else if (action === 'report') {
        this.reportDialog.showReport($container.data('report-url'));
      } else if (action === 'hide') {
        this.setItemAttibute($container, 'hidden', !$container.data('hidden'))
        remakePopover = true;
      } else if (action === 'stick') {
        this.setItemAttibute($container, 'stick', !$container.data('stick'))
        remakePopover = true;
      }

      var $popover = $container.find('.item-menu');
      if (remakePopover) {
        $popover.popover('destroy');
        $popover.data('popover-made', false);
      } else {
        $popover.popover('toggle');
      }
    }
  });
  window.ahr.market = window.ahr.market || {};
  window.ahr.market.initMarket = function (filters) {
    var filterView = new MarketFilterView({el: '#exchange-filters'});
//    var noResultsString = ['<p style="margin-top:20px;float:left;width:100%;text-align:center;" id="no-search-result">',
//        window.ahr.string_constants.market_search_no_match_a,
//        '<a href="#" id="searchagainall">',
//        window.ahr.string_constants.market_search_no_match_b + '</a>' + window.ahr.string_constants.market_search_no_match_c,
//        '<a href="#" id="searchwithdefaults">' ,
//        window.ahr.string_constants.market_search_no_match_d,
//        '</a></p>'].join(' ');
    var noResultsString = '<div style="text-align:center; font-size:20px; font-weight:bold">Your filter selection does not match any posts<div>';
    var market = new MarketView(
      {
        el: '#itemandsearchwrap',
        filterView: filterView,
        marketUrl: ahr.app_urls.getmarketitemfromto,
        noResultsString: noResultsString
      });
    market.initInfiniteScroll();
    document.title = window.ahr.string_constants.exchange;
  };

  window.ahr.market.initProfile = function(){
    var noResultsString = '<div style="text-align:center; font-size:20px; font-weight:bold">No posts created yet<div>';
    var market = new MarketView(
      {
        el: '#profile-view',
        marketUrl: ahr.app_urls.getusermarketitemsfromto,
        noResultsString: noResultsString
      });
    market.initInfiniteScroll();
  }

})();
