$(function () {
  var MarketFilterView = Backbone.View.extend({
    type: '',
    regions: [],
    skills: [],
    showHidden: false,

    events: {
      'click .type-menu a': 'setTypeFilter',
      'click .hidden-menu a': 'setHiddenFilter',
      'click .region-filter a': 'setRegionFilter',
      'click .skill-filter a': 'setSkillsFilter',
      'click a.search': 'toggleSearchControls',
      'click .run-search': 'triggerFilter',
      'keydown input[name=query]': 'checkForEnter',
      'shown.bs.popover a': 'setPopoverContent',
      'hide.bs.popover a': 'hidePopoverContent'
    },

    initialize: function(options) {
      var $skills = this.$el.find('a.skills');
      this.$skillsContainer = $skills.parent().find('.popover-container');
      this.skillsContent = _.template($('#skill-filter-list-template').html(), {skills: options.skills});
      $skills.popover({
        title: '',
        html: true,
        content: this.skillsContent,
        container: this.$skillsContainer,
        placement: 'bottom'
      });

      var $regions = this.$el.find('a.regions');
      this.$regionContainer = $regions.parent().find('.popover-container');
      this.regionsContent = _.template($('#region-filter-list-template').html())();
      $regions.popover({
        title: '',
        html: true,
        content: this.regionsContent,
        container: this.$regionContainer,
        placement: 'bottom'
      });

      this.$query = this.$el.find('input[name=query]');
    },

    setPopoverContent: function(ev) {
      var $currentTarget = $(ev.currentTarget);
      if ($currentTarget.hasClass('skills')) {
        this.$skillsContainer.find('.popover-content').html(this.skillsContent);
      } else {
        this.$regionContainer.find('.popover-content').html(this.regionsContent);
      }
    },

    hidePopoverContent: function (ev) {
      var $currentTarget = $(ev.currentTarget);
      if ($currentTarget.hasClass('skills')) {
        this.skillsContent = this.$skillsContainer.find('.popover-content').html();
      } else {
        this.regionsContent = this.$regionContainer.find('.popover-content').html();
      }
    },

    toggleSearchControls: function(ev) {
      var expand = this.$el.find('.search-expanded');
      this.$el.find('.search-expanded').toggleClass('hide');
      if (!expand.hasClass('hide')) {
        this.$query.focus();
      }
    },

    toggleFilterState: function(ev) {
      ev.preventDefault();
      var $target = $(ev.currentTarget);
      $target.toggleClass('selected');
      return {
        id: $target.data('id'),
        selected: $target.hasClass('selected'),
        value: $target.data('filter')
      };
    },

    setSkillsFilter: function (ev) {
      var skill = this.toggleFilterState(ev);
      if (skill.selected) {
        this.skills.push(skill.value);
      } else {
        this.skills = $.grep(this.skills, function (value) {
          return value != skill.value;
        });
      }
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

    checkForEnter: function(ev) {
      var key = ev.charCode ? ev.charCode : ev.keyCode ? ev.keyCode : 0;
      if (key === 13) {
        this.triggerFilter();
      }
    },

    triggerFilter: function() {
      this.trigger('filter');
    },

    setFilter: function(data) {
      if (this.type) {
        data.types = this.type;
      }
      if (this.skills) {
        data.skills = this.skills;
      }
      data.showHidden = this.showHidden;
      var query = this.$query.val();
      if (query) {
        data.search = query;
      }
    }
  });

  var PaginationView = Backbone.View.extend({
    marketView: null,
    pageSize: null,
    pageRange: null,
    pageActive: null,
    events: {
      "click .prev-page": "getPage",
      "click .page": "getPage",
      "click .next-page": "getPage"
    },

    getPage: function (e) {
      var that = this;
      e.preventDefault();
      var targetPage = $(e.currentTarget).data('page');
      var request = this.marketView.loadPage(targetPage);
      request.done(function () {
        that.render();
      });
    },
    updatePageState: function () {
      this.pageCount = this.marketView.pageCount;
      this.pageActive = this.marketView.pageActive;
      this.pageSize = this.marketView.pageSize;
    },

    initialize: function (options) {
      this.template = _.template($("#pagination_template").html());
      this.marketView = options.marketView;
      this.pageSize = options.pageSize;
      this.pageRange = options.pageRange;
      this.pageActive = options.pageActive;
    },

    render: function () {
      this.updatePageState();
      if (this.pageCount <= this.pageRange) {
        this.pageRange = this.pageCount;
      }
      var range = Math.floor(this.pageRange / 2);
      var navBegin = this.pageActive - range;
      if (this.pageRange % 2 == 0) {
        navBegin++;
      }
      var navEnd = this.pageActive + range;


      var leftDots = true;
      var rightDots = true;


      if (navBegin <= 2) {
        navEnd = this.pageRange;
        if (navBegin == 2) {
           navEnd++;
        }
        navBegin = 1;
        leftDots = false;
      }

      if (navEnd >= this.pageCount - 1) {
        navBegin = this.pageCount - this.pageRange + 1;
        if (navEnd == this.pageCount - 1) {
           navBegin--;
        }
        navEnd = this.pageCount;
        rightDots = false;
      }

      this.$el.html(this.template({
        link: this.link,
        pageCount: this.pageCount,
        pageActive: this.pageActive,
        navBegin: navBegin,
        navEnd: navEnd,
        leftDots: leftDots,
        rightDots: rightDots
      }));
      return this;
    },
    init: function () {
      var that = this;
      this.pageActive = 1;
      var request = this.marketView.loadPage(1);
      request.done(function () {
        return that.render();
      });
    }
  });

  var ProfileFilterView = Backbone.View.extend({
     setFilter: function(data) {
      data.showHidden = true;
    }
  })

  var MarketView = window.ahr.BaseView.extend({
    loadingPage: false,
    loadedOnce: false,
    currentCall: null,
    noResultsString: "",
    is_featured: false,
    $itemContainer: null,
    paginationView: null,

    types: {
      "Offers": "offer",
      "Request": "request"
    },

    events: {
      'click .market-place-item .item-menu': 'showMenuItem',
      'click .item-action-menu a': 'itemAction'
    },

    defaultOptions: {
      showHide: true,
      showSticky: true,
      item_tmp: '#item_template',
      item_menu_template: '#item-menu-template'
    },

    initialize: function (options) {
      options = _.extend({}, this.defaultOptions, options);
      this.options = options;
      this.item_type = 'item';
      this.getMarketItems = options.marketUrl;
      this.noResultsString = options.noResultsString;
      this.item_tmp = _.template($(options.item_tmp).html());
      this.$itemContainer = this.$el.find('.item-container');
      this.filterView = options.filterView;
      this.isProfile = options.isProfile || false;
      this.item_menu_template = _.template($(options.item_menu_template).html());
      this.closeDialog = new ahr.CloseItemDialogView();
      this.reportDialog = new ahr.ReportPostView();

      var $pagination = this.$el.find('.pagination');
      if ($pagination.length) {
        this.paginationView = new PaginationView({
          el: $pagination,
          marketView: this,
          pageRange: 3,
          pageActive: 1
        });

        if (this.filterView) {
          var that = this;
          this.filterView.on('filter', function () {
            that.paginationView.init();
          });
        }
      }

      this.refresh();

      return this;
    },

    refresh: function() {
      if (this.paginationView) {
        this.paginationView.init();
      } else {
        this.initNoPagination();
      }
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
        showSticky: this.options.showSticky,
        showHide: this.options.showHide,
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

    setItemAttibute: function($container, attribute, value, callback) {
      var data = {};
      data[attribute] = value;
      var onSuccess = function(){
        if (filterView && (attribute == 'hidden')) {
          filterView.trigger('filter');
        }
        if (callback) {
          callback();
        }
      };
      $.ajax({
        url: $container.data('attributes-url'),
        method: 'POST',
        context: this,
        data: data,
        success: onSuccess
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
        that.filterView.trigger('filter');
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
        this.setItemAttibute($container, 'stick', !$container.data('stick'), function () {
          if (stickyView) {
            stickyView.refresh();
          }
        });
        remakePopover = true;
      } else if (action === 'edit') {
        window.location.href = $container.data('edit-url');
      }

      var $popover = $container.find('.item-menu');
      if (remakePopover) {
        $popover.popover('destroy');
        $popover.data('popover-made', false);
      } else {
        $popover.popover('toggle');
      }
    },

    initNoPagination: function () {
      this.$el.find('.ajaxloader').show();
      this.$itemContainer.empty();
      var request = this.getItems();
      request.done(function (data) {
        this.render(data);
      });
    },

    clearMarketPage: function () {
      this.$itemContainer.empty();
      if (this.currentCall) {
        this.currentCall.abort();
        this.currentCall = null;
      }
      this.loadingPage = false;
    },

    loadPage: function (page) {
      if (!this.loadingPage) {
        this.loadingPage = true;

        this.clearMarketPage();
        this.$el.find('.ajaxloader').show();

        var dfrd = this.getItems(page);

        this.currentCall = dfrd;

        dfrd.done(function (data) {
          this.currentCall = null;
          this.render(data);
          this.loadingPage = false;
        });
        return dfrd;
      }
    },

    noSearchResult: function () {
      this.$itemContainer.append(this.noResultsString);
      this.$el.find('.pagination').hide();
    },

    getItems: function (page) {
      var data = {};
      if (this.filterView) {
        this.filterView.setFilter(data);
      }
      if (page) {
        data.page = page;
      }
      return $.ajax({
        url: this.getMarketItems,
        dataType: 'json',
        context: this,
        contentType: "application/json; charset=utf-8",
        data: data,
        traditional: true
      });
    },

    render: function (data) {
      this.$el.find('.ajaxloader').hide();
      var that = this;
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
          $('.tm-tag').each(function () {
            var txt = $('span', $(this)).text();
            $('.tag-button:contains(' + txt + ')').css('background-color', '#cccccc');
          });
        }
      });
      if (!hasItem) {
        this.noSearchResult();
      }
    }
  });

  var stickyView = null;
  var filterView = null;
  window.ahr.market = window.ahr.market || {};
  window.ahr.market.initMarket = function (options) {
    filterView = new MarketFilterView({el: '#exchange-filters', skills: options.skills});
    var noResultsString = '<div style="text-align:center; font-size:20px; font-weight:bold">Your filter selection does not match any posts</div>';
    var market = new MarketView({
      el: '#market-main',
      filterView: filterView,
      marketUrl: ahr.app_urls.getMarketItems,
      noResultsString: noResultsString
    });

    new MarketView({
      el: '#featured-marketitems',
      marketUrl: ahr.app_urls.getFeaturedMarketItems,
      noResultsString: '<div style="font-size: 16px; font-weight:bold">No featured items</div>',
      item_tmp: '#featured_item_template',
      showHide: false
    });

    stickyView = new MarketView({
      el: '#stuck-marketitems',
      marketUrl: ahr.app_urls.getStickyMarketItems,
      noResultsString: '<div style="font-size: 16px; font-weight:bold">You have no sticky items</div>'
    });
  };

  window.ahr.market.initProfile = function(userId){
    filterView = new ProfileFilterView()
    var noResultsString = '<div style="text-align:center; font-size:20px; font-weight:bold">No posts available<div>';
    var marketUrl = ahr.app_urls.getMarketItemsUser;

    if(userId) {
      marketUrl =  ahr.app_urls.getMarketItemsUser + userId;
    }

    new MarketView({
      el: '#profile-view',
      filterView: filterView,
      marketUrl: marketUrl,
      noResultsString: noResultsString,
      showSticky: false
    });
  }
});
