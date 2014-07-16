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
     $('#view-profile-menu').popover({
       title: '',
       html: true,
       content: $('#content-menu-template').html(),
       container: '#content-menu-container',
       placement: 'bottom'
     });

    $('#view-profile-menu').on('shown.bs.popover', function(){
      $('#view-profile-menu').addClass("active");
      $('#content-menu-container .popover').css("left", "-7px");
      $('#content-menu-container .arrow').css("left", "28px");
    });

    $('#view-profile-menu').on('hidden.bs.popover', function(){
      $('#view-profile-menu').removeClass("active");
    });
  }

  $("#sign-up-form").on('submit', function(ev){
    ev.preventDefault();
    var action_url = $(this).attr('action');
    var email = $(this).find('input').val();
    $.ajax({
      url: action_url,
      type: 'POST',
      dataType: 'json',
      data: {
        email: email
      },
      success: function(data){
        var r = data.result || "";
        var m = data.message || "Unable to process email at this time"
        $('#newsletter-conf').text(m);
        if(r === "success"){
          $("#sign-up-form").find('input').val("");
          $('#newsletter-conf').removeClass("alert-text");
        } else {
          $('#newsletter-conf').addClass("alert-text");
        }

      }
    });
  });

  setupAddPostPopover();
  setupProfileMenuPopover();
  $(document).ready(function() {
    doHeartBeat();
    $(document).on('doHeartBeat', function(){
      doHeartBeat();
    });
  });


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
