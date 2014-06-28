(function () {
  var AccordionView = Backbone.View.extend({
    el: 'body',
    events:{
      'click .select-multi-checkbox': 'multiCheckClick',
      'click .select-multi-checkbox label': 'multiCheckLabelClick',
      'click .select-checkbox': 'checkClick'
    },

    multiCheckLabelClick: function(ev){
      ev.stopPropagation();
      var currentState = $(ev.currentTarget).parent().find('input[type="checkbox"]').prop("checked");
      $(ev.currentTarget).parent().find('input[type="checkbox"]').prop("checked", !currentState);
      var countries = $(ev.currentTarget).closest('.row').next('.select-multi-items').find('input[type="checkbox"]');
      _.each(countries, function(country){
        $(country).prop("checked", !currentState);
        if(currentState){
          $(country).parent('.select-checkbox').removeClass("checked");
        } else {
          $(country).parent('.select-checkbox').addClass("checked");
        }
      });
      this.updateCounts();
    },

    multiCheckClick: function(ev){
      $(ev.currentTarget).toggleClass('selected');
      $(ev.currentTarget).closest('.row').next('.select-multi-items').toggle();
    },

    updateCounts: function(){
      var regions = $('.select-multi-checkbox');
      _.each(regions, function(region){
        var totalItems = $(region).closest('.row').next('.select-multi-items').find('input[type="checkbox"]').length;
        var checkedItems = $(region).closest('.row').next('.select-multi-items').find('input[type="checkbox"]:checked').length;
        if (totalItems === checkedItems) {
          $(region).find('.select-count').text("All Selected");
          $(region).find('input[type="checkbox"]').prop("checked", true);
        } else {
          $(region).find('.select-count').text(checkedItems + " Selected");
          $(region).find('input[type="checkbox"]').prop("checked", false);
        }
      });
    },

    checkClick: function(ev){
      if( $(ev.currentTarget).closest('.select-multi-items') ){
        this.updateCounts();
      }
    },


    initialize : function(){
      this.updateCounts();
      return this;
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initAccordionView = function () {
    var widget = new AccordionView();
  };
})();