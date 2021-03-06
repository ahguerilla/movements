/*
 * jQuery Tiny Pub/Sub
 * https://github.com/cowboy/jquery-tiny-pubsub
 *
 * Copyright (c) 2013 "Cowboy" Ben Alman
 * Licensed under the MIT license.
 */

if (!String.prototype.format) {
  String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
      return typeof args[number] != 'undefined' ? args[number] : match;
    });
  };
}

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

  function doHeartBeat() {
    if (window.ahr.user_id > 0) {
      $.getJSON(window.ahr.app_urls.heartbeat, function (data) {
        var notification_count = data.notifications || 0;
        var message_count = data.messages || 0;
        if (notification_count > 0) {
          $('#main-nav-count').text(notification_count);
          $('#main-nav-count').show();
        } else {
          $('#main-nav-count').text("");
          $('#main-nav-count').hide();
        }
        if (message_count > 0){
          $('#main-nav-message-count').text(message_count);
          $('#main-nav-message-count').show();
        } else {
          $('#main-nav-message-count').text("");
          $('#main-nav-message-count').hide();
        }
      });
    }
  }

  window.ahr.messageCounterWatch = function () {
    // check for new notification and messages
    // every 30 seconds
    if (window.ahr.user_id > 0) {
      setInterval(doHeartBeat, 30000);
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

    $('#add-post').on('shown.bs.popover', function(){
        $('#add-post-popup-container .popover').css("left", ($(document).screenX - 150).toString() + "px");
    });
  }

  function setupProfileMenuPopover() {
    var $viewProfileMenu = $('#view-profile-menu');
     $viewProfileMenu.popover({
       title: '',
       html: true,
       content: $('#content-menu-template').html(),
       container: '#content-menu-container',
       placement: 'bottom'
     });

    $viewProfileMenu.on('shown.bs.popover', function(){
      $('#view-profile-menu').addClass("active");
      $('#content-menu-container .popover').css("left", "-150px");
      $('#content-menu-container .arrow').css("left", "172px");
    });

    $viewProfileMenu.on('hidden.bs.popover', function(){
      $('#view-profile-menu').removeClass("active");
    });
  }

  setupAddPostPopover();
  setupProfileMenuPopover();
  $(document).ready(function() {
    doHeartBeat();
    $(document).on('doHeartBeat', function(){
      doHeartBeat();
    });
  });

  function applyErrorsToForm(form, response, $messageOutput) {
    var errorLabelFmt = '<label for="id_{0}" class="error">{1}</label>';
    var genericMessage = response.detail;
    var msg, errorDiv, input, errorLabel = null;
    form.find('.error').hide();
    if (response.errors) {
      for (var inputName in response.errors) {
        msg = response.errors[inputName].join(' ');
        errorLabel = errorLabelFmt.format("inputName", msg);
        errorDiv = form.find('.' + inputName + '-errors');
        if (errorDiv.length) {
          errorDiv.html(errorLabel);
        } else {
          input = form.find('input[name="' + inputName + '"]');
          $(errorLabel).insertAfter(input);
        }

      }
    }
    if (genericMessage) {
      $messageOutput.html(JST.userMessage({
        message: genericMessage,
        dismissable: true,
        level: 'danger'
      }));
    }
  }
  window.ahr.applyErrorsToForm = applyErrorsToForm;


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
