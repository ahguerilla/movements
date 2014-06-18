(function () {
  var MarketFilterView = Backbone.View.extend({
    type: '',
    regions: [],
    skills: [],

    events: {
      'click .type-menu a': 'setTypeFilter',
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
    }
  });

  var MarketView = window.ahr.market.MarketBaseView.extend({
    types: {
      "Offers": "offer",
      "Request": "request"
    },

    events: {
      'click .market-place-item .item-menu': 'showMenuItem'
    },

    initialize: function (options) {
      this.item_type = 'item';
      this.getitemfromto = window.ahr.app_urls.getmarketitemfromto;
      this.item_tmp = _.template($('#item_template').html());
      this.init(options.filterView);
      this.item_menu_template = _.template($('#item-menu-template').html());
      return this;
    },

    showMenuItem: function(ev) {
      var $link = $(ev.currentTarget);
      if ($link.data('popover-made')) {
        return;
      } else {
        ev.preventDefault();
        var $container = $link.parent();
        var content = this.item_menu_template({hasEdit: $link.data('has-edit')});
        $link.popover({
          title: '',
          html: true,
          content: content,
          container: $container,
          placement: 'bottom'
        });
        $link.popover('show');
        $link.data('popover-made', true);
      }
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.market = window.ahr.market || {};
  window.ahr.market.initMarket = function (filters) {
    var filterView = new MarketFilterView({el: '#exchange-filters'});
    var market = new MarketView({el: '#itemandsearchwrap', filterView: filterView});
    market.initInfiniteScroll();
    document.title = window.ahr.string_constants.exchange;
  };

})();
