$(function () {
  var MarketFilterView = Backbone.View.extend({
    type: '',
    regions: [],
    skills: {selected: [], rootClass: '.skill-filter'},
    issues: {selected: [], rootClass: '.issue-filter'},
    showHidden: false,

    events: {
      'click .type-menu a': 'setTypeFilter',
      'click .hidden-filter a': 'setHiddenFilter',
      'click .region-filter > li > a': 'showCountries',
      'click .country-list a.back': 'showRegions',
      'click .country-list a.country': 'setRegionFilter',
      'click .country-list a.country-all': 'setRegionFilter',
      'click .skill-filter a': 'setSkillsFilter',
      'click .issue-filter a': 'setIssuesFilter',
      'click a.search': 'clickToggleSearch',
      'click .run-search': 'triggerFilter',
      'keydown input[name=query]': 'checkForEnter',
      'show.bs.popover a': 'setActive',
      'shown.bs.popover a': 'setPopoverContent',
      'hide.bs.popover a': 'hidePopoverContent'
    },

    initialize: function(options) {
      this.$query = this.$el.find('input[name=query]');
      // build the structure from the query string
      this.setFiltersFromQueryString();
      var self = this;
      var $skills = this.$el.find('a.skills');
      this.skills.$container = $skills.parent().find('.popover-container');

      // used to set defaults from query string
      _.each(options.skills, function(skill){
        if(_.contains(self.skills.selected, skill.pk.toString())){
          skill.selected = "selected";
        } else {
          skill.selected = "";
        }
      });
      var otherSkillSelected = false;
      if(_.contains(self.skills.selected, "-1" )){
        otherSkillSelected = true;
      }
      var allSkillsSelected = false;
      if(this.skills.selected.length > options.skills.length){
        allSkillsSelected = true;
      }
      var skillArgs = {
        allSkillsSelected: allSkillsSelected,
        otherSkillSelected: otherSkillSelected,
        skills: options.skills
      };
      this.skills.content = _.template($('#skill-filter-list-template').html(), skillArgs);
      this.skills.count = options.skills.length;
      this.skills.$count = $skills.find('.count');
      this.updateCount(this.skills);
      $skills.popover({
        title: '',
        html: true,
        content: this.skills.content,
        container: this.skills.$container,
        placement: 'bottom'
      });
      $skills.click(function(ev){
        ev.preventDefault();
      });

      var $issues = this.$el.find('a.issues');
      this.issues.$container = $issues.parent().find('.popover-container');

      // used to set defaults from query string
      _.each(options.issues, function(issue){
        if(_.contains(self.issues.selected, issue.pk.toString())){
          issue.selected = "selected";
        } else {
          issue.selected = "";
        }
      });
      var otherIssueSelected = false;
      if(_.contains(self.issues.selected, "-1" )){
        otherIssueSelected = true;
      }
      var allIssuesSelected = false;
      if(this.issues.selected.length > options.issues.length){
        allIssuesSelected = true;
      }
      var issuesArgs = {
        allIssuesSelected: allIssuesSelected,
        otherIssueSelected: otherIssueSelected,
        skills: options.issues
      };
      this.issues.content = _.template($('#issue-filter-list-template').html(), issuesArgs);
      this.issues.count = options.issues.length;
      this.issues.$count = $issues.find('.count');
      this.updateCount(this.issues);
      $issues.popover({
        title: '',
        html: true,
        content: this.issues.content,
        container: this.issues.$container,
        placement: 'bottom'
      });
      $issues.click(function(ev){
        ev.preventDefault();
      });

      var $regions = this.$el.find('a.regions');
      this.$regionContainer = $regions.parent().find('.popover-container');
      this.$regionsCount = $regions.find('.count');
      this.regionsCount = parseInt($regions.data('country-count'));
      this.regionsContent = $('#region-filter-list-template').html();

      // update the selected countries
      var $regionsHtml = $(this.regionsContent);
      _.each(this.regions, function(r){
         $regionsHtml.find("[data-filter='" + r + "']").addClass('selected');
      });
      var countryLists = $regionsHtml.find('.country-list');
      _.each(countryLists, function(c){
        self.setRegionalCounts($(c));
      });
      this.setRegionCounts();

      this.regionsContent = "<ul class=\"region-filter\">" + $regionsHtml.html() + "</ul>";
      $regions.popover({
        title: '',
        html: true,
        content: this.regionsContent,
        container: this.$regionContainer,
        placement: 'bottom'
      });
      $regions.click(function(ev){
        ev.preventDefault();
      });

      var $hidden = this.$el.find('a.showhide');
      this.$hiddenContainer = $hidden.parent().find('.popover-container');
      this.hiddenContent = $('#hidden-filter-template').html();
      $hidden.popover({
        title: '',
        html: true,
        content: this.hiddenContent,
        container: this.$hiddenContainer,
        placement: 'bottom'
      });
      $hidden.click(function(ev){
        ev.preventDefault();
      });

      if(options.defaultFilters){
        if(options.defaultFilters.type) {
          this.type = options.defaultFilters.type;
          this.toggleType(this.type);
        }
      }
    },

    setActive: function(ev) {
      var $currentTarget = $(ev.currentTarget);
      $currentTarget.parents('li').addClass('active');
    },

    setPopoverContent: function(ev) {
      var $currentTarget = $(ev.currentTarget);
      if ($currentTarget.hasClass('skills')) {
        this.skills.$container.find('.popover-content').html(this.skills.content);
      } else if ($currentTarget.hasClass('issues')) {
        this.issues.$container.find('.popover-content').html(this.issues.content);
      }else if ($currentTarget.hasClass('regions')) {
        this.$regionContainer.find('.popover-content').html(this.regionsContent);
      } else {
        this.$hiddenContainer.find('.popover-content').html(this.hiddenContent);
      }
    },

    hidePopoverContent: function (ev) {
      var $currentTarget = $(ev.currentTarget);
      $currentTarget.parents('li').removeClass('active');
      if ($currentTarget.hasClass('skills')) {
        this.skills.content = this.skills.$container.find('.popover-content').html();
      } else if ($currentTarget.hasClass('issues')) {
        this.issues.content = this.issues.$container.find('.popover-content').html();
      } else if ($currentTarget.hasClass('regions')) {
        this.regionsContent = this.$regionContainer.find('.popover-content').html();
      } else {
        this.hiddenContent = this.$hiddenContainer.find('.popover-content').html();
      }
    },

    clickToggleSearch: function(ev) {
      ev.preventDefault();
      this.toggleSearchControls();
    },

    toggleSearchControls: function() {
      this.$el.toggleClass('search-expanded');
      var $currentTarget = $('a.search');
      $currentTarget.parents('li').toggleClass('active');
      var expand = this.$el.find('.search-expanded');
      this.$el.find('.search-expanded').toggleClass('hide');
      if (!expand.hasClass('hide')) {
        this.$query.focus();
      }
    },

    showCountries: function(ev) {
      ev.preventDefault();
      var $currentTarget = $(ev.currentTarget);
      if ($currentTarget.hasClass('region-all')) {
        var setSelected = (this.regionsCount != this.regions.length);
        var $countryLists = $currentTarget.parents('.region-filter').find('.country-list');
        _.each($countryLists, function(countryList) {
          var $countryList = $(countryList);
          this.setRegionAll($countryList, setSelected)
          this.setRegionalCounts($countryList);
        }, this);
        this.setRegionCounts();
        this.trigger('filter');
      } else {
        var $countryList = $currentTarget.parent().find('.country-list');
        var $topLevel = $currentTarget.parents('.region-filter');
        $topLevel.addClass('expanded');
        $countryList.removeClass('hide');
      }
    },

    showRegions: function(ev) {
      ev.preventDefault();
      var $currentTarget = $(ev.currentTarget);
      var $countryList = $currentTarget.parents('.country-list');
      var $topLevel = $currentTarget.parents('.region-filter');
      $topLevel.removeClass('expanded');
      $countryList.addClass('hide');
    },

    toggleFilterState: function(ev, $target) {
      if (ev) {
        ev.preventDefault();
        $target = $(ev.currentTarget);
      }
      $target.toggleClass('selected');
      return {
        $target: $target,
        id: $target.data('id'),
        selected: $target.hasClass('selected'),
        value: $target.data('filter')
      };
    },

    setFlatFilter: function(ev, data) {
      var item = this.toggleFilterState(ev);
      if (item.value == 'all') {
        if (data.selected.length == (data.count + 1)) {
          data.selected = [];
          this.$el.find(data.rootClass + ' a').removeClass('selected');
        } else {
          data.selected = [];
          item.$target.addClass('selected');
          _.each(this.$el.find(data.rootClass + ' a.skill-normal'), function (elem) {
            var $elem = $(elem);
            data.selected.push($elem.data('filter'));
            $elem.addClass('selected');
          }, this);
        }
      } else {
        if (item.selected) {
          data.selected.push(item.value);
          if (data.selected.length == data.count) {
            this.$el.find(data.rootClass + ' .skill-all').addClass('selected');
          }
        } else {
          this.$el.find(data.rootClass + ' .skill-all').removeClass('selected');
          data.selected = $.grep(data.selected, function (value) {
            return value != item.value;
          });
        }
      }
      this.updateCount(data);
      this.trigger('filter');
    },

    updateCount: function (data){
      if (data.selected.length) {
        data.$count.html('(' + data.selected.length + ')');
        data.$count.show();
      } else {
        data.$count.hide();
      }
    },

    setIssuesFilter: function (ev) {
      this.setFlatFilter(ev, this.issues);
    },

    setSkillsFilter: function (ev) {
      this.setFlatFilter(ev, this.skills);
    },

    setRegion: function(region) {
      if (region.selected) {
        this.regions.push(region.value)
      } else {
        this.regions = $.grep(this.regions, function (value) {
          return value != region.value;
        });
      }
    },

    setRegionAll: function($countryList, setSelected) {
      _.each($countryList.find('.country'), function (country) {
        var $country = $(country);
        if ((setSelected && !$country.hasClass('selected')) || (!setSelected && $country.hasClass('selected'))) {
          this.setRegion(this.toggleFilterState(null, $country));
        }
      }, this);
    },

    setRegionCounts: function() {
      if (this.regions.length) {
        this.$regionsCount.html('(' + this.regions.length + ')');
        this.$regionsCount.show();
      } else {
        this.$regionsCount.hide();
      }
      if (this.regionsCount == this.regions.length) {
        this.$el.find('.region-all').addClass('selected');
      } else {
        this.$el.find('.region-all').removeClass('selected');
      }
    },

    setRegionalCounts: function($countryList) {
      var fullCount = parseInt($countryList.data('country-count'));
      var $count = $countryList.parents('.region-top').find('.count');
      var selected = $countryList.find('.country.selected').length;
      if (selected) {
        $count.html('(' + selected + ')');
        $count.show();
      } else {
        $count.hide();
      }

      var $countryAll = $countryList.find('.country-all');
      if (selected == fullCount) {
        $countryAll.addClass('selected');
      } else {
        $countryAll.removeClass('selected');
      }
    },

    setRegionFilter: function(ev) {
      var region = this.toggleFilterState(ev);
      var $countryList = region.$target.parents('.country-list');
      var fullCount = parseInt($countryList.data('country-count'));

      if (region.value == 'all') {
        var currentlySelected = $countryList.find('.country.selected').length;
        var setSelected = (currentlySelected != fullCount);
        this.setRegionAll($countryList, setSelected);
      } else {
        this.setRegion(region);
      }

      this.setRegionalCounts($countryList);
      this.setRegionCounts();

      this.trigger('filter');
    },

    setHiddenFilter: function(ev) {
      var showHidden = this.toggleFilterState(ev);
      this.showHidden = showHidden.selected;
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

    toggleType: function(type) {
      this.$el.find('.type-menu li.active').removeClass('active');
      this.$el.find('.type-menu a[data-filter="' + type + '"]').parents('li').addClass('active');
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
      if (this.skills.selected) {
        data.skills = this.skills.selected;
      }
      if (this.issues.selected) {
        data.issues = this.issues.selected;
      }
      if (this.regions) {
        data.countries = this.regions;
      }
      data.showHidden = this.showHidden;
      var query = this.$query.val();
      if (query) {
        data.search = query;
      }
      this.buildFilterQueryString();
    },

    buildFilterQueryString: function(){
      var queryMap = {};
      if (this.type) {
        queryMap['type'] = this.type;
      }
      if (this.skills.selected) {
        queryMap['skills'] = this.skills.selected;
      }
      if (this.issues.selected) {
        queryMap['issues'] = this.issues.selected;
      }
      if (this.regions) {
        queryMap['regions'] = this.regions;
      }
      var query = this.$query.val();
      if (query) {
         queryMap['search'] = query;
      }
      var queryString = $.param(queryMap);
      if (queryString) {
        window.location.hash = '#' + queryString;
      } else {
        window.location.hash = '';
      }
    },

    setFiltersFromQueryString: function(){
      var hash = (window.location.hash).substring(1);
      var queryMap = $.deparam(hash);
      if ('type' in queryMap) {
        this.type = queryMap['type'];
        this.toggleType(this.type);
      }
      if ('skills' in queryMap) {
        this.skills.selected = queryMap['skills'];
      }
      if ('issues' in queryMap) {
        this.issues.selected = queryMap['issues'];
      }
      if ('regions' in queryMap) {
        this.regions = queryMap['regions'];
      }
      if ('search' in queryMap) {
        this.$query.val(queryMap['search']);
        this.toggleSearchControls();
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
  });

  var MarketView = window.ahr.BaseView.extend({
    loadingScrollElements: false,
    currentItem: 0,
    itemsPerCall: 12,
    loadingPage: false,
    loadedOnce: false,
    currentCall: null,
    noResultsString: "",
    is_featured: false,
    $itemContainer: null,
    paginationView: null,
    userDefaultLangage: 'en',

    types: {
      "Offers": "offer",
      "Request": "request"
    },

    events: {
      'click .market-place-item .item-menu': 'showMenuItem',
      'click .item-action-menu a': 'itemAction',
      'click .share-twitter': 'shareTwitter'
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
      this.getitemfromto = ahr.app_urls.getmarketitemfromto;
      this.getMarketItems = options.marketUrl;
      this.noResultsString = options.noResultsString;
      this.item_tmp = _.template($(options.item_tmp).html());
      this.$itemContainer = this.$el.find('.item-container');
      this.filterView = options.filterView;
      this.isProfile = options.isProfile || false;
      this.item_menu_template = _.template($(options.item_menu_template).html());
      this.closeDialog = new ahr.CloseItemDialogView();
      this.reportDialog = new ahr.ReportPostView();
      this.userDefaultLangage = options.userDefaultLangage;

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
//            that.paginationView.init();
            that.initInfiniteScroll();
          });
        }
      }

      this.refresh();

      return this;
    },

    shareTwitter: function(ev) {
      ev.preventDefault();

      // url is (up to) 23 char, 140 total... 117 left for message, including automatic space separator.

      var postUrl = ev.currentTarget.href;
      var preamble = "New on #Movements: \"";
      var postTitle = $(ev.currentTarget).closest(".market-place-item").find(".title").text();
      var comment = preamble + postTitle + "\"";
      if (comment.length > 116) {
        comment = comment.substring(0, 112) + "...\"";
      }
      var twitterUrl = "https://twitter.com/share?url=" + encodeURIComponent(postUrl) + "&text=" + encodeURIComponent(comment);
      this.openTwitterPopup(twitterUrl);
    },

    openTwitterPopup: function(url){
      var width  = 575,
        height = 400,
        left   = ($(window).width()  - width)  / 2,
        top    = ($(window).height() - height) / 2,
        opts   = 'status=1' +
                 ',width='  + width  +
                 ',height=' + height +
                 ',top='    + top    +
                 ',left='   + left;

      window.open(url, 'twitter', opts);
    },

    refresh: function() {
      if (this.paginationView) {
//        this.paginationView.init();
        this.initInfiniteScroll();
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
      ev.preventDefault();
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


    unpublishPost: function(url){
      $.ajax({
        url: url,
        method: 'POST',
        context: this,
        success: function(){
          if(this.filterView){
            this.filterView.trigger('filter');
          }
        }
      });
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
      };

      var remakePopover = false;
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
      } else if (action === 'unpublish') {
        this.unpublishPost($container.data('unpublish-url'));
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

    initInfiniteScroll: function () {
      $('#marketitems').empty();
      if (this.currentCall) {
        this.currentCall.abort();
        this.currentCall = null;
      }
      this.allItemsLoaded = false;
      this.currentItem = 0;
      this.currentPage = 1;
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

    clearMarketPage: function () {
      this.$itemContainer.empty();
      if (this.currentCall) {
        this.currentCall.abort();
        this.currentCall = null;
      }
      this.loadingPage = false;
    },

    loadScrollElements: function () {
      var that = this;
      if (!that.loadingScrollElements && that.levelReached(30) && !that.allItemsLoaded) {
        that.loadingScrollElements = true;

        that.$el.find('.ajaxloader').show();

        var dfrd = this.getItems(this.currentPage);

        this.currentCall = dfrd;

        dfrd.done(function (data) {
          that.currentCall = null;
          that.render(data);

          if (data.length === 1) {
            that.allItemsLoaded = true;
          }

          that.currentPage = that.currentPage + 1;
          that.loadingScrollElements = false;

          // Gets more results if not enough to fill tall screens.
          that.loadScrollElements();
        });
        return dfrd;
      }
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

    getItemsFromTo: function (from, to) {
      var data = {};
      if (this.filterView) {
        this.filterView.setFilter(data);
      }
      return $.ajax({
        url: this.getitemfromto.replace('0', from) + to,
        dataType: 'json',
        context: this,
        contentType: "application/json; charset=utf-8",
        data: data,
        traditional: true
      });
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
          var theItem = item;
          if (item.fields.translate_language_url && (item.fields.language != that.userDefaultLangage)) {
            $.ajax({
              url: item.fields.translate_language_url,
              type: 'GET',
              dataType: 'json',
              success: function (data) {
                if(data.response === "success") {
                  var post = $('.market-place-item[data-item-id="' + data.itemid + '"]');
                  if (post) {
                    post.find('.title').text(data.title_translated);
                    if (data.status == 4) {
                      post.find('.user-translated-text span').html(data.username);
                      post.find('.user-translated-text').show();
                    } else {
                      if (data.status == 3) {
                        post.find('.auto-translated-text span').show();
                      }
                      post.find('.auto-translated-text').show();
                    }
                  }
                }
              }
            });
          }
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
    var filterViewArgs = {
      el: '#exchange-filters',
      skills: options.skills,
      issues: options.issues,
      defaultFilters: options.filters
    };
    filterView = new MarketFilterView(filterViewArgs);
    var noResultsString = '<div style="text-align:center; font-size:20px; font-weight:bold">Finished loading posts</div>';
    var market = new MarketView({
      el: '#market-main',
      filterView: filterView,
      marketUrl: ahr.app_urls.getMarketItems,
      noResultsString: noResultsString,
      userDefaultLangage: options.userDefaultLangage
    });

    new MarketView({
      el: '#featured-marketitems',
      marketUrl: ahr.app_urls.getFeaturedMarketItems,
      noResultsString: '<div style="font-size: 16px; font-weight:bold">No featured items</div>',
      item_tmp: '#featured_item_template',
      userDefaultLangage: options.userDefaultLangage,
      showHide: false
    });

    stickyView = new MarketView({
      el: '#stuck-marketitems',
      marketUrl: ahr.app_urls.getStickyMarketItems,
      noResultsString: '<div style="font-size: 16px; font-weight:bold">You have no sticky items</div>',
      userDefaultLangage: options.userDefaultLangage
    });
  };

  window.ahr.market.initProfile = function(options){
    filterView = new ProfileFilterView()
    var noResultsString = '<div style="text-align:center; font-size:20px; font-weight:bold">Finished loading posts<div>';
    var marketUrl = ahr.app_urls.getMarketItemsUser;

    if(options.userId) {
      marketUrl =  ahr.app_urls.getMarketItemsUser + options.userId;
    }

    new MarketView({
      el: '#profile-view',
      filterView: filterView,
      marketUrl: marketUrl,
      noResultsString: noResultsString,
      showSticky: false,
      userDefaultLangage: options.userDefaultLangage
    });
  }
});
