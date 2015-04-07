(function(global) {

  var TranslationsView = Backbone.View.extend({
    events: {
      'click .for-approval .accept-translation': 'approvalAction',
      'click .for-approval .reject-translation': 'approvalAction'
    },

    initialize: function(options) {
      this.loaderHtml = _.template($('#loader-template').html())();
      this.options = options;
      this.getUserTranslations();
      this.getAvailableTranslations();
      if (options.is_cm) {
        this.getTranslationsForApproval();
      }
    },

    getUserTranslations: function() {
      $.ajax({
        context: this,
        dataType: 'json',
        url: this.options.getUserTranslationsUrl,
        success: this.renderUserTranslations
      });
    },

    renderUserTranslations: function(data) {
      var tpl = _.template($('#user-translations-template').html());
      this.$el.find('.in-progress .list').html(tpl(data));
    },

    getAvailableTranslations: function () {
      $.ajax({
        context: this,
        dataType: 'json',
        url: this.options.getAvailableTranslationsUrl,
        success: this.renderAvailableTranslations
      });
    },

    renderAvailableTranslations: function(data) {
      var tpl = _.template($('#available-translations-template').html());
      this.$el.find('.needed .list').html(tpl(data));
    },

    getTranslationsForApproval: function () {
      $.ajax({
        context: this,
        dataType: 'json',
        url: this.options.getTranslationsForApprovalUrl,
        success: this.renderTranslationsForApproval
      });
    },

    renderTranslationsForApproval: function (data) {
      var tpl = _.template($('#translations-for-approval-template').html());
      this.$el.find('.for-approval .list').html(tpl(data));
    },


    approvalAction: function(ev) {
      var $currentTarget = $(ev.currentTarget);
      var url = $currentTarget.data('url');
      var $container = $currentTarget.closest('.translation');
      $container.html(this.loaderHtml);
      $.ajax({
        url: url,
        context: this,
        data: {
          lang_code: $container.data('code')
        },
        type: 'post',
        success: function() {
          $container.remove();
          if (this.$el.find('.for-approval .translation').length == 0) {
            this.renderTranslationsForApproval({translations: []});
          }
        }
      });
    }
  });

  global.ahr.translations = {
    TranslationsView: TranslationsView
  }
})(window);
