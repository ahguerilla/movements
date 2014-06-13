(function (global) {

  var CreatePostView = Backbone.View.extend({
    events: {
      'click .select-checkbox': 'checkClick'
    },
    checkClick: function (ev) {
      $(ev.currentTarget).find('input[type="checkbox"]').prop("checked", !$(ev.currentTarget).find('input[type="checkbox"]').prop("checked"));
      $(ev.currentTarget).toggleClass("checked");
    }
  });

  global.ahr.initCreatePost = function() {
    new CreatePostView({el: '.new-post'});
  };

})(this);
