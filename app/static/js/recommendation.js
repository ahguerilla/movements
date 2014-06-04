(function(){
    $('.nanamorde').hide();
    var RecommendationView = window.ahr.BaseView.extend({
      el: $('#preview'),

      get: function(data){
        var itemHtml = this.item_tmp(data);
        var $itemHtml = $(itemHtml);
        $itemHtml = $itemHtml.clickUrl();
        return $itemHtml;
      },

      isSingle: function () {
        return (true);
      },

      initialize : function(data){
        that=this;
        this.obj_type = data.obj_type;
        this.obj_id   = data.obj_id;

        this.getItem = window.ahr.app_urls.getmarketitem;
        this.item_tmp = _.template($('#item_template').html());

        this.item_widget    = window.ahr.marketitem_widget.initWidget('body', this, null, null);
        this.profile_widget = window.ahr.profile_widget.initWidget(null, window.ahr.app_urls.getprofile);

        var dfrd = $.ajax({url: this.getItem + this.obj_id});
        dfrd.done(function (item) {
          var html = that.get(_.extend(item[0].fields,{'isSingle': true}));
          if ($(window).width() >= 992) {
            $('.nanamorde').show();
          } else {
            $('.nanamorde-mobile').show();
          }

          $('#singleItem').html(html);
          that.item_widget.afterset();

          that.profile_widget.set(item[0].fields.owner[0],'.userprofile', 'user');
          $('#singleItem').show();
        });

        return this;
      },
    });
    window.ahr = window.ahr || {};
    window.ahr.recommendation = window.ahr.recommendation || {};
    window.ahr.recommendation.initRecommendation = function(obj_type, obj_id){
        window.ahr.recommendationview = new RecommendationView({'obj_type':obj_type, 'obj_id':obj_id});
        document.title = window.ahr.string_constants.recommendation;
    };
})();
