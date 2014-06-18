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

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
      // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      var csrftoken = $.cookie('csrftoken');
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

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

  var $currentPopover = null;
  $(document).on('shown.bs.popover', function (ev) {
    var $target = $(ev.target);
    if ($currentPopover && ($currentPopover.get(0) != $target.get(0))) {
      $currentPopover.popover('toggle');
    }
    $currentPopover = $target;
  });

  $(document).on('hidden.bs.popover', function (ev) {
    var $target = $(ev.target);
    if ($currentPopover && ($currentPopover.get(0) == $target.get(0))) {
      $currentPopover = null;
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

  function setupProfileMenuPopover() {
     $('#view-profile-menu').popover({
       title: '',
       html: true,
       content: $('#content-menu-template').html(),
       container: '#content-menu-container',
       placement: 'bottom'
     });

    $('#view-profile-menu').on('shown.bs.popover', function(){
      $('#content-menu-container .popover').css("left", 0);
      $('#content-menu-container .arrow').css("left", "28px");
    });
  }

  setupAddPostPopover();
  setupProfileMenuPopover();

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
