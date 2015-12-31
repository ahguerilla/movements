(function () {
  var HomeView = Backbone.View.extend({
    el: '.landing-page-center-content-wrap',
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
          this.$el.find('#home_stats').html(this.buildStatsBanner(data));
          this.$el.fadeIn('slow');
        },
        error: function () {}
      });
    },
    buildStatsBanner: function(data) {
      return data.connections + " Human Rights Connections made Among " + data.user + " Active Users from " + data.countries + " Countries";
    }

  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initStats = function () {
    new HomeView();
  };
})();