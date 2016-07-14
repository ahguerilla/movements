(function (global) {

  var ShareDialogView = Backbone.View.extend({
    events: {
      'click .facebook': 'shareFacebook'
    },

    shareFacebook: function(ev){
      ev.preventDefault();
      var postUrl = $(ev.currentTarget).data('href');
      if(postUrl) {
        postUrl = window.ahr.siteData.baseUrl + postUrl;
      }  else {
        postUrl = ev.currentTarget.href;
      }
      var facebookUrl = 'http://www.facebook.com/sharer.php?p[url]=' + postUrl;
      this.openPopup(facebookUrl);
    },

    openPopup: function(url){
      var width  = 575,
        height = 400,
        left   = ($(window).width()  - width)  / 2,
        top    = ($(window).height() - height) / 2,
        opts   = 'status=1' +
                 ',width='  + width  +
                 ',height=' + height +
                 ',top='    + top    +
                 ',left='   + left;

      window.open(url, 'twitter', opts);
    }

  });

  global.ahr.initShareDialog = function (options) {
    new ShareDialogView(options);
  }
})(window);