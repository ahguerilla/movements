/*
 * jQuery Tiny Pub/Sub
 * https://github.com/cowboy/jquery-tiny-pubsub
 *
 * Copyright (c) 2013 "Cowboy" Ben Alman
 * Licensed under the MIT license.
 */

(function($) {

  var o = $({});

  $.subscribe = function() {
    o.on.apply(o, arguments);
  };

  $.unsubscribe = function() {
    o.off.apply(o, arguments);
  };

  $.publish = function() {
    o.trigger.apply(o, arguments);
  };

}(jQuery));


(function () {
  window.ahr.messageCounterWatch = function () {
    if (window.ahr.user_id > 0) {
      setInterval(function () {
        var text;
        $.getJSON(window.ahr.app_urls.getmessagecount, function (data) {
          $('.message-counter').each(function (tmp, item) {
            if (data > 0) {
              $('#msgcntr', $(item)).text('(' + data + ')');
            } else {
              $('#msgcntr', $(item)).text('');
            }
          });
        });
      }, 60000);
    }
  };

  function toggleNav() {
    if ($('#bs-example-navbar-collapse-1').hasClass('in')) {
      $(".navbar-toggle").click();
    }
  }

  var lastsize = $(window).width();
  $(window).on({
    "orientationchange": function (event) {
      toggleNav();
    },
    "resize": function (event) {
      var thissize = $(window).width();

      if (lastsize < 992 && thissize >= 992) {
        toggleNav();
      }
      lastsize = thissize;
    }
  });

  function setupAddPostPopover() {
    $('#add-post').popover({
      title: '',
      html: true,
      content: $('#add-post-template').html(),
      container: '#add-post-popup-container',
      placement: 'bottom'
    });
  }

  function setupContentMenuPopover() {
     $('#view-content-menu').popover({
       title: '',
       html: true,
       content: $('#content-menu-template').html(),
       container: '#content-menu-container',
       placement: 'bottom'
     });

    $('#view-content-menu').on('shown.bs.popover', function(){
      $('#content-menu-container .popover').css("left", 0);
      $('#content-menu-container .arrow').css("left", "28px");
    });
  }

  setupAddPostPopover();
  //setupContentMenuPopover();

  window.ahr.BaseView = Backbone.View.extend({
    events: {},
    showModalDialog: function (templateId, templateData, dialogId, callback) {
      var tmpl = _.template($(templateId).html());
      var tmpl_html = tmpl(templateData);
      $('#modal-placeholder').html(tmpl_html);
      $(dialogId).modal('show');
      if (callback) {
        $(dialogId).on('shown.bs.modal', callback);
      }
    },

    invert: function (obj) {
      var new_obj = {};
      for (var prop in obj) {
        if (obj.hasOwnProperty(prop)) {
          new_obj[obj[prop]] = prop;
        }
      }
      return new_obj;
    },

    alert: function (message, selector) {
      window.ahr.alert(message, selector);
    },

    clearalert: function (selector) {
      window.ahr.clearalert(selector);
    },

    info: function (message, selector) {
      $(selector).empty();
      $(selector).prepend('<div class="alert alert-success alert-dismissable">' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
        message + '</div>');
    }
  });
})();
