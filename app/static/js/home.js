(function () {
  var HomeView = Backbone.View.extend({
    el: '.landing-page-center-content-wrap',
    isLogin: true,
    events: {
      'click .home_signup': 'clickHomeSignup',
      'click .home_cancel': 'clickHomeCancel',
      'submit #home_login_form': 'submitHomeLoginForm'
    },
    initialize: function() {
      this.loadStats();
    },

    submitHomeLoginForm: function(ev) {
      ev.preventDefault();
      if(this.isLogin){
        this.loginFromHome();
      } else {
        this.signupFromHome();
      }
    },
    loginFromHome: function() {
      this.clearError();
      var email = this.$el.find('#home_login_form').find('input[name=email]').val();
      var password = this.$el.find('#home_login_form').find('input[name=password1]').val();
      if (!email || !password) {
        this.displayError(["All fields are required."]);
        return;
      }

      $.ajax({
        type: 'POST',
        url: window.ahr.app_urls.apiLoginUrl,
        data: this.$el.find('#home_login_form').serialize(),
        context: this,
        success: function(data){
          if(data.success) {
            window.location.reload();
          } else {
            this.displayError(data.errors);
          }
        }
      });
    },
    signupFromHome: function() {
      this.clearError();
      var email = this.$el.find('#home_login_form').find('input[name=email]').val();
      var password1 = this.$el.find('#home_login_form').find('input[name=password1]').val();
      var password2 = this.$el.find('#home_login_form').find('input[name=password2]').val();
      if (!email || !password1 || !password2) {
        this.displayError(["All fields are required."]);
        return;
      }
      $.ajax({
        type: 'POST',
        url: window.ahr.app_urls.apiSignupStart,
        data: this.$el.find('#home_login_form').serialize(),
        context: this,
        success: function(data){
          if(data.success) {
            window.location.href = data.next;
          } else {
            this.displayError(data.errors);
          }
        }
      });
    },
    displayError: function(errorList) {
      var errorString = "";
      _.each(errorList, function(error){
        errorString += error + '<br>';
      });
      this.$el.find('.invalid-login').html(errorString).show();
    },
    clearError: function(){
      this.$el.find('.invalid-login').html('&nbsp;').hide();
    },
    clickHomeSignup: function(ev) {
      ev.preventDefault();
      this.isLogin = false;
      this.clearError();
      this.$el.find('#home_page_buttons').slideUp();
      this.$el.find('.password_repeat').slideDown();
      this.$el.find('.login_buttons').slideUp();
      this.$el.find('.login_or_signup_text').text(window.ahr.string_constants.signup_text);
      this.$el.find('.submit_continue').slideDown();
    },
    clickHomeCancel: function(ev) {
      ev.preventDefault();
      this.isLogin = true;
      this.clearError();
      this.$el.find('#home_page_buttons').slideDown();
      this.$el.find('.password_repeat').slideUp();
      this.$el.find('.login_buttons').slideDown();
      this.$el.find('.login_or_signup_text').text(window.ahr.string_constants.signup_login_text);
      this.$el.find('.submit_continue').slideUp();
    },
    loadStats: function() {
      $.ajax({
        url: window.ahr.app_urls.getStats,
        type: 'GET',
        dataType: 'json',
        context: this,
        success: function (data){
          this.$el.find('#home_stats').html(this.buildStatsBanner(data));
          this.$el.fadeIn('slow');
        },
        error: function () {}
      });
    },
    buildStatsBanner: function(data) {
      var ctx = {
        connections: window.ahr.addCommasToNumber(data.connections),
        users: window.ahr.addCommasToNumber(data.user),
        countries:  window.ahr.addCommasToNumber(data.countries)
      };
      return JST.home_page_stats(ctx);
    }

  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initHome = function () {
    new HomeView();
  };
})();