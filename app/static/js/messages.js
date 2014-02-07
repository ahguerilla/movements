(function () {
  var InboxRoute = Backbone.Router.extend({
    routes: {
      "": "page",
      "p:page": "page"
    },
    page: function (page) {
      $.noop();
    },
    initialize: function (market) {
      $.noop();
    }
  });

  var InboxView = Backbone.View.extend({
    el: '#postman',
    events: {
      'click .conv_link': 'openConv',
      'click #back': 'back',
      'click .next': 'addNext'
    },

    addNext: function (ev) {
      ev.preventDefault();
      var dfrd = $.ajax({
        url: ev.currentTarget.href
      });
      dfrd.done(function (data) {
        if ($('.next', $(data)).hasClass('disabled')) {
          $('#paginationblock').remove();
        }
        $('.messagelist').append($('.messagelist', $(data)).children());
      });
    },

    reply: function (ev) {
      ev.reventDefault();
      return false;
    },

    openConv: function (ev) {
      var that = this;
      ev.preventDefault();
      if (ev.currentTarget.parentElement.tagName == "STRONG") {
        a = ev.currentTarget;
        $(ev.currentTarget.parentElement).html(a);
      }

      var dfrd = $.ajax({
        url: ev.currentTarget.href,
        dataType: 'html'
      });

      dfrd.done(function (data) {
        data1 = data.replace(that.itemre, function (match, item_id, offset, string) {
          return "<a href='/market/#item/" + item_id + "'>Click here to view the recommendation</a>";
        });
        data2 = data1.replace(that.userre, function (match, username, offset, string) {
          return "<a href='" + window.ahr.app_urls.viewuserprofile + username + "'>Click here to view the recommendation</a>";
        });

        data3 = data2.replace(that.itemre, function (match, item_id, offset, string) {
          return " ";
        });
        data4 = data3.replace(that.userre, function (match, item_id, offset, string) {
          return " ";
        });
        $('#conversation').html(data4);
        $('#id_body').empty();
        window.ahr.expandTextarea('#id_body');
        that.showconv();
        $.getJSON(window.ahr.app_urls.getmessagecount, function (data) {
          $('.message-counter').each(function (tmp, item) {
            if (data > 0) {
              $('#msgcntr', $(item)).text('(' + data + ')');
            } else {
              $('#msgcntr', $(item)).text('');
            }
          });
        });


      });
      return false;
    },

    showconv: function () {
      if ($(window).width() < 992) {
        $("#message-col").hide();
        $('#conversation').show();
        $('#back').show();
        $('body').scrollTop(0);
      } else {
        $('body').scrollTop(0);
      }
    },

    back: function (ev) {
      $('#conversation').hide();
      $("#message-col").show();
      $('#back').hide();
    },

    resize: function (ev) {
      if ($(window).width() < 992 && $('#conversation').css('display') != 'none' && $("#message-col").css('display') != 'none') {
        $('#conversation').hide();
      } else if ($(window).width() >= 992) {
        if ($('#conversation').css('display') == 'none') {
          $('#conversation').show();
          $($('.conv_link')[0]).trigger('click');
        }
        $('#conversation').show();
        $('#back').hide();
        $("#message-col").show();
      }
    },

    initialize: function () {
      $(window).resize(this.resize);
      var more = $('.next')[0];
      this.itemre = new RegExp(/&lt;!--item=&quot;(\d+)&quot;--&gt;/);
      this.userre = new RegExp(/&lt;!--user=&quot;(\S+)&quot;--&gt;/);
      $(more).html('<button class="btn btn-primary">more...</button>');
      $('#paginationblock').html(more);
      this.resize();
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.messages = window.ahr.messages || {};
  window.ahr.messages.initInbox = function () {
    var messages = new InboxView();
    var messages_route = new InboxRoute(messages);
    if ($(window).width() > 992) {
      $($('.conv_link')[0]).trigger('click');

    }
    $('#back').hide();
    Backbone.history.start();
  };
})();