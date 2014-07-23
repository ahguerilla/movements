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

        var template_data = {
          'termConditionsText': $(resp).find('.cms-body-content').html(),
          'acceptCheck': $('#accept_terms_tpl').html()
        };
        var termsContent = _.template($('#accept_terms_page_tpl').html(), template_data);
        that.$acceptTerms.prop('checked', false);
        $.colorbox({
          html: termsContent
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
