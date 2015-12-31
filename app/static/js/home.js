(function () {
  var HomeView = Backbone.View.extend({
    el: '.landing-page-center-content-wrap',
    events: {
      'click .home_login': 'clickHomeLogin',
      'click .home_signup': 'clickHomeSignup',
      'click .home_cancel': 'clickHomeCancel'
    },
    initialize: function() {
      this.loadStats();
    },
    clickHomeLogin: function(ev) {
      ev.preventDefault();
      var formType = $(ev.currentTarget).data('type');
      $.ajax({
        type: 'POST',
        url: window.ahr.app_urls.loginUrl,
        data: this.$el.find('#' + formType + '_login').serialize(),
        context: this,
        success: function(data){
          if(data.success) {
            window.location.reload();
          } else {
            this.$el.find('.invalid-login').show();
          }
        }
      });
    },
    clickHomeSignup: function(ev) {
      ev.preventDefault();
      var formType = $(ev.currentTarget).data('type');
      if (formType === 'central') {
        this.$el.find('#home_page_buttons').slideUp();
      }
      this.$el.find('.password_repeat').slideDown();
      this.$el.find('.login_buttons').slideUp();
      this.$el.find('.login_or_signup_text').text(window.ahr.string_constants.signup_text);
      this.$el.find('.submit_continue').slideDown();
    },
    clickHomeCancel: function(ev) {
      ev.preventDefault();
      var formType = $(ev.currentTarget).data('type');
      if (formType === 'central') {
        this.$el.find('#home_page_buttons').slideDown();
      }
      this.$el.find('.password_repeat').slideUp();
      this.$el.find('.login_buttons').slideDown();
      this.$el.find('.login_or_signup_text').text(window.ahr.string_constants.signup_login_text);
      this.$el.find('.submit_continue').slideUp();
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
  window.ahr.widgets.initHome = function () {
    new HomeView();
  };
})();