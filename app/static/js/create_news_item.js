(function (global) {
  var CreateNewsItemView = Backbone.View.extend({
    existing: null,
    events: {
      'click #parse_news_url': 'clickGo',
      'click .select-checkbox': 'checkClick'
    },
    initialize: function() {
      this.$newsItemTemplate = _.template($('#news-item-card-template').html());
    },
    setInitial: function(args) {
      if (args) {
        this.existing = args;
        this.parseNewsUrl();
      } else {
        var url = this.$el.find('#id_news_url').val();
        if (url.length > 0) {
          this.parseNewsUrl();
        }
      }
    },
    checkClick: function(ev) {
      $(ev.currentTarget).find('input[type="checkbox"]').prop("checked", !$(ev.currentTarget).find('input[type="checkbox"]').prop("checked"));
      $(ev.currentTarget).toggleClass("checked");
    },
    clickGo: function(ev) {
      ev.preventDefault();
      this.parseNewsUrl();
    },
    parseNewsUrl: function() {
      if(this.existing){
        this.$el.find('#news_item').html(this.$newsItemTemplate(this.existing));
        this.$el.find('#news_item_post_details').show();
        return;
      }
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
              this.$el.find('#news_item_post_details').show();
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

  global.ahr.initCreateNewsItem = function(args) {
    var newsView = new CreateNewsItemView({el: '#create-post-form'});
    newsView.setInitial(args)
  };

})(window);
