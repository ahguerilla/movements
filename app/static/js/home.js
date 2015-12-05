(function () {
  var StatsView = Backbone.View.extend({
    el: '.stats-banner',
    initialize: function() {
      this.loadStats();
    },
    loadStats: function() {
      $.ajax({
        context: this,
        url: window.ahr.app_urls.getStats,
        type: 'GET',
        dataType: 'json',
        success: function (data){
          this.$el.html(this.buildStatsBanner(data));
          this.$el.fadeIn('slow');
        },
        error: function () {}
      });
    },
    buildStatsBanner: function(data) {
      var banner = '<h3>' + window.ahr.string_constants.stats_stats + '</h3>' +
                   '<div class="stat">' + window.ahr.string_constants.stats_connections_made  +
                   ':&nbsp;<span>' + data.connections + '</span></div>' +
                   '<div class="stat">' + window.ahr.string_constants.stats_active_users  +
                   ':&nbsp;<span>' + data.user + '</span></div>' +
                   '<div class="stat">' + window.ahr.string_constants.stats_countries_represented  +
                   ':&nbsp;<span>' + data.countries + '</span></div>';

      return banner;
    }

  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initStats = function () {
    new StatsView();
  };
})();