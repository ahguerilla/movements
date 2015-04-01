(function(global) {

  var TranslationsView = Backbone.View.extend({
    initialize: function(options) {
      this.options = options;
      this.getUserTranslations();
      this.getAvailableTranslations();
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
    }
  });

  global.ahr.translations = {
    TranslationsView: TranslationsView
  }
})(window);
