(function () {
  var InboxView = Backbone.View.extend({
    el: '#postman',
    events: {
      'click .conv_link': 'openConv',
      'click #backtofolder': 'back'
    },

    postProcessConv: function(data){
      var that = this;
      var data1 = data.replace(that.itemre, function (match, item_id, offset, string) {
        return "<a href='/market/#item/" + item_id + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });
      var data2 = data1.replace(that.userre, function (match, username, offset, string) {
        return "<a href='" + window.ahr.app_urls.viewuserprofile + username + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });

      var data3 = data2.replace(that.itemre, function (match, item_id, offset, string) {
        return "<a href='/market/#item/" + item_id + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });
      var data4 = data3.replace(that.userre, function (match, username, offset, string) {
        return "<a href='" + window.ahr.app_urls.viewuserprofile + username + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });

      var user = null;
      $('.messageavatar img', data4).each(function (item, index) {
        user = $(this).attr('alt');
        if (user != window.ahr.username) return false;
      });
      if (user == window.ahr.username) {
        user = $('.pm_recipient', data4).text();
        if (user =="<me>") user = window.ahr.username;
      }
      return ({'user':user, 'html':data4});
    },

    setMessageCounter: function(){
      $.getJSON(window.ahr.app_urls.getmessagecount, function (data) {
        $('.message-counter').each(function (tmp, item) {
          if (data > 0) {
            $('#msgcntr', $(item)).text('(' + data + ')');
          } else {
            $('#msgcntr', $(item)).text('');
          }
        });
      });
    },

    openConv: function (ev) {
      ev.preventDefault();
      $('#conversation').hide();
      var that = this;
      var subject = $('.subject', $(ev.currentTarget)).children();
      if (subject.is('strong')) {
        subject.replaceWith(subject.text());
      }

      if (ev.currentTarget.parentElement.tagName == "STRONG") {
        a = ev.currentTarget;
        $(ev.currentTarget.parentElement).html(a);
      }

      var dfrd = $.ajax({
        url: ev.currentTarget.getAttribute('href'),
        dataType: 'html'
      });

      dfrd.done(function (data) {
        var conv = that.postProcessConv(data);
        $('#conversation').html(conv.html);
        if ($('#id_body').length > 0) {
          $('#id_body').empty();
          window.ahr.expandTextarea('#id_body');
        }
        that.showconv();
        that.setMessageCounter();
      });
      return false;
    },

    showconv: function () {
      $('#conversation').show();
      $('#conversation-cont').show();
      $('#back').show();
      $('#breadsubject').text($('#messagesubjectheader').text());
      $('body').scrollTop(0);
    },

    back: function (ev) {
      $('#conversation-cont').hide();
      $('#back').hide();
    },

    initialize: function () {
      this.actions_view = window.ahr.actions_view();
      this.itemre = new RegExp(/&lt;!--item=&quot;(\d+)&quot;--&gt;/);
      this.userre = new RegExp(/&lt;!--user=&quot;(\S+)&quot;--&gt;/);
      $('#conversation-cont').hide();
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.messages = window.ahr.messages || {};
  window.ahr.messages.initInbox = function () {
    new InboxView();
    $('#back').hide();
  };
})();