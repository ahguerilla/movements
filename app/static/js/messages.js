(function () {
  var InboxView = Backbone.View.extend({
    el: '#postman',
    folderType: 'inbox',
    leftColBaseHeight: 0,
    events: {
      'click #reply-btn': 'replyToConversation',
      'click .sidebar .message': 'openConversationFromClick',
      'click #conversation .message-header a': 'stopBubble',
      'click #conversation .message-header': 'toggleMessage',
      'rezie #conversation': 'resizeSideBar'
    },

    stopBubble: function(ev) {
      ev.stopPropagation();
    },

    postProcessConv: function(data){
      var that = this;
      var data1 = data.replace(that.itemre, function (match, item_id, offset, string) {
        return "<a href='/market/" + item_id + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });
      var data2 = data1.replace(that.userre, function (match, username, offset, string) {
        return "<a href='" + window.ahr.app_urls.viewuserprofile + username + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });

      var data3 = data2.replace(that.itemre, function (match, item_id, offset, string) {
        return "<a href='/market/" + item_id + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });
      var data4 = data3.replace(that.userre, function (match, username, offset, string) {
        return "<a href='" + window.ahr.app_urls.viewuserprofile + username + "'>" + window.ahr.string_constants.view_recommendation + "</a>";
      });

      var user = null;
      if (user == window.ahr.username) {
        user = $('.pm_recipient', data4).text();
        if (user =="<me>") user = window.ahr.username;
      }
      return ({'user':user, 'html':data4});
    },

    openConversationFromClick: function(ev) {
      ev.preventDefault();
      this.openConversation($(ev.currentTarget));
    },

    openConversation: function ($message) {
      $('#conversation').html('');

      this.$el.find('.sidebar .message').removeClass('selected');
      $message.addClass('selected');
      if (this.folderType == 'inbox') {
        if ($message.hasClass('new')) $message.removeClass('new');
      }

      $.ajax({
        url: $message.attr('href'),
        dataType: 'html',
        context: this,
        success: function(data) {
          var conv = this.postProcessConv(data);
          $('#conversation').html(conv.html);
          if ($('#id_body').length > 0) {
            $('#id_body').empty();
            window.ahr.expandTextarea('#id_body');
          }
          this.showconv();
        }
      });

      return false;
    },

    showconv: function () {
      $('#conversation').show();
      $('body').scrollTop(0);
    },

    replyToConversation: function(ev) {
      ev.preventDefault();
      if ($('#id_body').val() != "") {
        $('#replyform').submit();
      } else {
        alert('{%trans "You cant send an empty message."%}');
      }
      return false;
    },

    toggleMessage: function(ev) {
      var $messageBody = $(ev.currentTarget).parents('.message').find('.message-body');
      $messageBody.toggleClass('collapse');
    },

    initialize: function () {
      this.itemre = new RegExp(/&lt;!--item=&quot;(\d+)&quot;--&gt;/);
      this.userre = new RegExp(/&lt;!--user=&quot;(\S+)&quot;--&gt;/);
      this.folderType = this.$el.data('folder-type');
      $('#conversation').html('');

      this.leftColBaseHeight = this.$el.find('.sidebar').height();

      var $messages = this.$el.find('.sidebar .message:first-child');
      if ($messages.length) this.openConversation($messages);

      this.$el.find('#conversation').css('min-height', this.$el.find('.sidebar').height());
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.messages = window.ahr.messages || {};
  window.ahr.messages.initInbox = function () {
    new InboxView();
  };
})();