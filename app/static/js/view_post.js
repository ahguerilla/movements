(function (global) {

  var PostView = Backbone.View.extend({
    events: {
      'submit .comments form': 'submitComment',
      'click .report': 'showReportForm'
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

      $('.translate span').on('shown.bs.popover', function() {
        $('.language-selector ul li').click(function () {
          var translate_url = $(this).data("translate_url");
          if (translate_url) {
            $.ajax({
              url: translate_url,
              type: 'GET',
              dataType: 'json',
              success: function (data) {
                // todo: make this more robuts (error case etc)
                $('#post-title').text(data.title);
                $('#post-body').text(data.details);
                //$('.translate span').modal('hide')
              }
            });
          }
        });
      });
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
    }
  });

  global.ahr.initViewPost = function (options) {
    new PostView({el: '.view-post', getCommentsUrl: options.getCommentsUrl, addCommentUrl: options.addCommentUrl});
  };

})(window);
