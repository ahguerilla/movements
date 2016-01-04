(function (global) {
  var CreateNewsItemView = Backbone.View.extend({
    events: {
      'click #parse_news_url': 'parseNewsUrl'

    },
    initialize: function() {
      this.$newsItemTemplate = _.template($('#news-item-card-template').html());
    },
    parseNewsUrl: function(ev) {
      ev.preventDefault();

      var self = this;
      var displayError = function(error) {
        if (error) {
          self.$el.find('.news_url-errors').html('<div class="error">' + error + '<div>');
          self.$el.find('#news_item').html('');
        } else {
          self.$el.find('.news_url-errors').html('');
          self.$el.find('#news_item').html('');
        }
      };
      displayError();
      this.$el.find('#news_item').html('');
      var url = this.$el.find('#id_news_url').val();
      if (url.length > 0) {
        this.$el.find('#news_item').html('<div style="text-align: center;"><i class="fa fa-2x fa-spinner fa-spin"></i></div>');
        $.ajax({
          type: 'POST',
          url: window.ahr.app_urls.parseNewsItem,
          data: {url: url},
          context: this,
          success: function(data){
            if(data.success) {
              this.$el.find('#news_item').html(this.$newsItemTemplate(data));
            } else {
              displayError('Please enter a valid url');
            }
          },
          error: function(){
            displayError('Error parsing url');
          }
        });
      } else {
        displayError('Please enter a valid url');
      }
    }
  });

  global.ahr.initCreateNewsItem = function() {
    new CreateNewsItemView({el: '#create-post-form'});
  };

})(window);
