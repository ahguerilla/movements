(function () {
  var MoreAboutYouWidget = Backbone.View.extend({
    el: '.more-about-you-widget',
    steps: null,
    stepsOrder: null,
    events: {
      'click .next-button': 'clickNextButton',
      'click .select-checkbox': 'checkClick',
      'click .skip-link': 'skipAction',
      'click #create-offer-button': 'clickCreateOfferButton',
      'click #create-request-button': 'clickCreateRequestButton',
      'click #create-post-later': 'createLater'
    },

    initialize: function(options) {
      this.steps = options.steps;
    },

    clickCreateOfferButton: function(ev){
      ev.preventDefault();
      this.$el.find('#id_user_preference_type_0').attr('checked', true);
      this.$el.find('#id_post_type').val('1');
      $(ev.currentTarget).closest('form').submit();
    },

    clickCreateRequestButton: function(ev) {
      ev.preventDefault();
      this.$el.find('#id_user_preference_type_1').attr('checked', true);
      this.$el.find('#id_post_type').val('2');
      $(ev.currentTarget).closest('form').submit();
    },

    createLater: function(ev) {
      ev.preventDefault();
      this.$el.find('#id_post_type').val('0');
      $(ev.currentTarget).closest(".step").hide();
      $(ev.currentTarget).closest(".step").next(".step").show();
      window.scrollTo(0, 0);
    },

    renderSteps: function() {
      var selected = $("#id_user_preference_type input[type='radio']:checked").val();
      if (selected == 0) { // offer
        this.stepsOrder = [0, 3, 1, 2, 4];
      } else if  (selected == 1) {
        this.stepsOrder = [0, 1, 2, 3, 4];
      } else {
        this.stepsOrder = [0, 3, 1, 2, 4];
      }
      var args = {
        'stepsOrder': this.stepsOrder,
        'steps': this.steps
      };
      this.$el.find('.progress-counter').html(JST.more_about_you_progress_bar(args));
      this.$el.find('.progress-counter').show();
    },

    clickNextButton: function(ev){
      ev.stopPropagation();
      ev.preventDefault();
      if($(ev.currentTarget).hasClass('render-steps')) {
        this.renderSteps();
      }

      // hide current step and show next
      $(ev.currentTarget).closest(".step").hide();

      // toggle progress bar
      var currentItem = $(".progress-item.current");
      currentItem.removeClass("current").addClass("complete");
      currentItem.find("span").html("&#10004;");

      var nextItem = currentItem.next(".progress-item")
      if(nextItem){
        $(nextItem).removeClass("outstanding").addClass("current");
      }

      // show the correct step
      var currentId = nextItem.attr('id').split('-')[2];
      $('#step' + currentId).show();
      window.scrollTo(0, 0);

    },

    checkClick: function(ev){
      $(ev.currentTarget).find('input[type="checkbox"]').prop("checked", !$(ev.currentTarget).find('input[type="checkbox"]').prop("checked"));
      $(ev.currentTarget).toggleClass("checked");
    },
    skipAction: function (ev) {
      ev.stopPropagation();
      ev.preventDefault();
      $(ev.currentTarget).closest('form').submit();
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initMoreAboutYou = function (options) {
    new MoreAboutYouWidget(options);
  };
})();
