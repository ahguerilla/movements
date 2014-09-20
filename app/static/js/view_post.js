(function (global) {

  var PostView = Backbone.View.extend({
    events: {
      'submit .comments form': 'submitComment',
      'click .report': 'showReportForm',
      'click .delete-comment': 'deleteComment',
      'click .tweet': 'shareTwitter'
    },
    initialize: function(options) {
      this.options = options;
      this.$commentsLoading = this.$el.find('.comment-list .loader');
      this.$commentListContent = this.$el.find('.comment-list .content');
      this.$commentListTemplate = _.template($('#comment-list-template').html());
      this.$commentText = this.$el.find('.comments form textarea');
      this.$submitButton = this.$el.find('.comments form button');
      this.loadComments();

      this.report_widget = new window.ahr.ReportPostView();
      this.linkifyContent();
      this.initTranslatePopup();

      // Auto-Google-Translate the post title and body.
      var translate_url = $(".view-post").data('default_translate_url');
      if (translate_url) {
        $.ajax({
          url: translate_url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            if(data.response === "success") {
              $('#post-title').html(data.title);
              if ($('#post-body').html() != data.details) {
                $('#post-body-translated').html(data.details);
                $('#via-google-translate').attr('style', '');
              }
              else
              {
                $('#post-body-translated').html('');
                $('#via-google-translate').attr('style', 'display: none;');
              }
            } else {
              $('#post-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
            }
            $('.translate span').popover('hide');
          },
          error: function (){
            $('#post-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
            $('.translate span').popover('hide');
          }
        });
      }
    },
    linkifyContent: function(){
      var toLinkify = $('.linkify');
      var autolinker = new Autolinker({
        newWindow: true,
        stripPrefix: false,
        truncate: 50
      });
      _.each(toLinkify, function(item) {
        var textToLink = $(item).text();
        $(item).html(autolinker.link(textToLink));
      });
    },
    initTranslatePopup: function(){
      $('.translate span').popover({
        title: '',
        html: true,
        content: $('#translate-menu-template').html(),
        container: '#translate-menu-container',
        placement: 'top'
      });
      var self = this;
      $('.translate span').on('shown.bs.popover', function() {
        $('.language-selector ul li').click(function () {
          var translate_url = $(this).data("translate_url");
          if (translate_url) {
            $.ajax({
              url: translate_url,
              type: 'GET',
              dataType: 'json',
              success: function (data) {
                if(data.response === "success") {
                  $('#post-title').html(data.title);
                  if ($('#post-body').html() != data.details) {
                    $('#post-body-translated').html(data.details);
                    $('#via-google-translate').attr('style', '');
                  }
                  else
                  {
                    $('#post-body-translated').html('');
                    $('#via-google-translate').attr('style', 'display: none;');
                  }
                  self.linkifyContent();
                } else {
                  $('#post-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
                }
                $('.translate span').popover('hide');
              },
              error: function (){
                $('#post-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
                $('.translate span').popover('hide');
              }
            });
          }
        });
      });
    },

    shareTwitter: function(ev) {
      ev.preventDefault();

      // url is (up to) 23 char, 140 total... 117 left for message, including automatic space separator.

      var postUrl = ev.currentTarget.href;
      var preamble = "New on #Movements: \"";
      var postTitle = document.getElementById('post-title').innerText;
      var comment = preamble + postTitle + "\"";
      if (comment.length > 116) {
        comment = comment.substring(0, 112) + "...\"";
      }
      var twitterUrl = "https://twitter.com/share?url=" + encodeURIComponent(postUrl) + "&text=" + encodeURIComponent(comment);
      this.openTwitterPopup(twitterUrl);
    },

    openTwitterPopup: function(url){
      var width  = 575,
        height = 400,
        left   = ($(window).width()  - width)  / 2,
        top    = ($(window).height() - height) / 2,
        opts   = 'status=1' +
                 ',width='  + width  +
                 ',height=' + height +
                 ',top='    + top    +
                 ',left='   + left;

      window.open(url, 'twitter', opts);
    },

    showReportForm: function(ev){
      ev.preventDefault();
      this.report_widget.showReport(ev.currentTarget.getAttribute('report_url'));
    },
    loadComments: function() {
      this.$submitButton.removeAttr('disabled');
      this.$commentsLoading.show();
      $.ajax({
        context: this,
        dataType: 'json',
        url: this.options.getCommentsUrl,
        success: this.renderCommentList,
        error: this.problemFetchingComments
      });
    },
    renderCommentList: function(comments) {
      var rendered  = this.$commentListTemplate({comments: comments});
      this.$commentListContent.html(rendered)
      this.$commentsLoading.hide();
    },
    problemFetchingComments: function() {
      this.$commentsLoading.hide();
      this.$commentListContent.html('There was a problem fetching the comments');
    },
    submitComment: function(ev) {
      ev.preventDefault();
      var contents = this.$commentText.val();
      this.$commentText.val('');
      this.$submitButton.attr('disabled', 'disabled');
      $.ajax({
        context: this,
        method: 'post',
        dataType: 'json',
        url: this.options.addCommentUrl,
        data: {
          contents: contents
        },
        success: this.loadComments
      })
    },
    deleteComment: function(ev) {
      var $comment = $(ev.currentTarget);
      ev.preventDefault();
      var commentId = $comment.closest('.comment').attr('comment_id');
      if(!commentId){
        return;
      }
      $.ajax({
        context: this,
        method: 'post',
        dataType: 'json',
        url: this.options.deleteCommentUrl,
        data: {
          commentID: commentId
        },
        success: function(data) {
          if (data.success == true) {
            $comment.closest('.comment').remove();
          }
        }
      })
    }
  });

  global.ahr.initViewPost = function (options) {
    new PostView({el: '.view-post', getCommentsUrl: options.getCommentsUrl, addCommentUrl: options.addCommentUrl, deleteCommentUrl: options.deleteCommentUrl});
  };

})(window);
