(function () {
  "use strict";

  var SignupWidget = Backbone.View.extend({
    el: '#signup_form',
    events: {
      'click button[type=submit]': 'preventDoubleClick'
    },

    preventDoubleClick: function (e) {
      $(e.currentTarget).prop('disabled', true);
      this.$el.submit();
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initSignup = function () {
    var widget = new SignupWidget();
  };
})();
