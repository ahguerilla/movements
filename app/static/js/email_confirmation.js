(function () {
  "use strict";

  var ConfirmationWidget = Backbone.View.extend({
    el: 'body',
    events: {
      'click .terms': 'showTerms',
      'change input[name=colorbox_accept_terms]': 'closeTerms'
    },

    showTerms: function (e) {
      e.preventDefault();
      var request = $.get($(e.currentTarget).attr('href')),
        that = this;
      request.done(function (resp) {
        that.$acceptTerms.prop('checked', false);
        $.colorbox({
          width: "100%",
          height: '100%',
          html: $(resp).find('.content-page').html() + $('#accept_terms_tpl').html()
        });
      });
    },

    closeTerms: function (e) {
      var that = this;
      if ($(e.currentTarget).prop('checked')) {
        that.$acceptTerms.prop('checked', true);
        $.colorbox.remove();
      }
    },

    initialize: function () {
      this.$acceptTerms = $('input[name=accept_terms]');
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initConfirmation = function () {
    var widget = new ConfirmationWidget();
  };
})();
