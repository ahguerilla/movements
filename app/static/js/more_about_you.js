(function () {
  var MoreAboutYouWidget = Backbone.View.extend({
    el: '.more-about-you-widget',

    events: {
      'click .next-button': 'clickNextButton'
    },

    clickNextButton: function(ev){
      ev.stopPropagation();
      ev.preventDefault();
      // hide current step and show next
      $(ev.currentTarget).closest(".step").hide();
      $(ev.currentTarget).closest(".step").next(".step").show();

      // toggle progress bar
      var currentItem = $(".progress-item.current");
      currentItem.removeClass("current").addClass("complete");
      currentItem.find("span").html("&#10004;");

      var nextItem = currentItem.next(".progress-item")
      if(nextItem){
        $(nextItem).removeClass("outstanding").addClass("current");
      }
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initMoreAboutYou = function () {
    var widget = new MoreAboutYouWidget();
  };
})();
