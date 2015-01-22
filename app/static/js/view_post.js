(function (global) {

  var PostView = Backbone.View.extend({
    events: {
      'submit .comments form': 'submitComment',
      'click .report': 'showReportForm',
      'click .delete-comment': 'deleteComment',
      'click .tweet': 'shareTwitter',
      'click .translated_by a': 'changeTranslation',
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
              var user_lang = translate_url.replace('?human=false', '').slice(-3, -1);
              if(user_lang === data.source_language){
                $('#post-body-translated').text('');
                $('div.translated_by').hide();
              } else {
                $('#post-title').text(data.title);
                $('#post-body-translated').text(data.details);
                if (data.status == 4) {
                  $('div.translated_by a.user').html(data.username).attr('data-translate_url', translate_url);
                  $('div.translated_by a.google').attr('data-translate_url', translate_url + '?human=false');
                  $('div.translated_by span').show();
                } else {
                  $('div.translated_by span').hide();
                  $('div.translated_by a.google').attr('data-translate_url', '');
                }
                $('div.translated_by').show();
              }
            } else {
              $('#post-body-translated').html('<p><span style="color:red">Unable to provide translation</span></p>');
            }
          },
          error: function (){
            $('#post-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
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
            self.translate(translate_url);
          }
        });
      });
    },

    translate: function(translate_url) {
      var self = this;
      $.ajax({
        url: translate_url,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          if(data.response === "success") {
            var trans_lang = translate_url.replace('?human=false', '').slice(-3, -1);
            $('#post-title').text(data.title);
            if(trans_lang === data.source_language){
              $('#post-body-translated').text("");
              $('div.translated_by').hide();
            } else {
              $('#post-body-translated').text(data.details);
              if (data.status == 4) {
                $('div.translated_by a.user').html(data.username).attr('data-translate_url', translate_url);
                $('div.translated_by a.google').attr('data-translate_url', translate_url + '?human=false');
                $('div.translated_by span').show();
              } else if (!data.human_aviable) {
                $('div.translated_by span').hide();
                $('div.translated_by a.user').attr('data-translate_url', '');
              }
              $('div.translated_by').show();
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
    },

    changeTranslation: function(ev) {
      ev.preventDefault();
      var url = $(ev.currentTarget).data('translate_url');
      if (url) {
        this.translate(url);
      }
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

  TranslationData = Backbone.Model.extend({

    defaults: {
      is_translator: false,
      is_cm: false,
      active: false,
      status: null,
      correction: false,
      take_in_url: null,
      take_off: null,
      mark_done: null,
      approval_url: null,
      revoke_url: null,
      correction_url: null,
      details_translated: '',
      title_translated: '',
      prev_title: null,
      prev_text: null,
      display_title: null,
      display_text: null,
    },
  });

  TranslateView = Backbone.View.extend({
    el: $('#translation-container'),

    events: {
        "click button#take_in": "TakeIn",
        "click button#done": "Done",
        "click button#take_off": "Take_off",
        "click button#confirm": "Confirm",
        "click button#revoke": "Revoke",
        "click button#edit": "Edit",
        "click button#correction": "Correction",
    },

    initialize: function(options){
      this.$areaTemplate = _.template($('#translation-area').html());
      this.data = new TranslationData();
      this.data.set(options);
      this.initTranslationPopup();
      this.render();
    },

    render: function(){
      var self = this;
      console.log(this.data.attributes);
      if (this.data.get('status') == 3) {

        // title
        var diff = JsDiff.diffChars(self.data.get('prev_title'), self.data.get('title_translated'));
        var display_title= '';
        diff.forEach(function(part){
          var color = part.added ? 'green' :
            part.removed ? 'red' : 'grey';
          display_title += '<span style="color:' + color + ';">' + part.value + '</span>'
        });
        self.data.set('display_title', display_title);

        // description
        var diff = JsDiff.diffChars(self.data.get('prev_text'), self.data.get('details_translated'));
        var display_text= '';
        diff.forEach(function(part){
          var color = part.added ? 'green' :
            part.removed ? 'red' : 'grey';
          display_text += '<span style="color:' + color + ';">' + part.value + '</span>'
        });
        self.data.set('display_text', display_text);
      }
      this.$el.html( this.$areaTemplate(this.data.attributes) );
      this.$form = this.$el.find('form');
    },

    initTranslationPopup: function(){
      var popup_element = $('li .translate');
      popup_element.popover({
        title: '',
        html: true,
        content: $('#translator-menu-template').html(),  // using simple as translate, but need urls to be changed
        container: '#translation-menu-container',
        placement: 'top'
      });
      var self = this;
      popup_element.on('shown.bs.popover', function() {
        $('.language-selector ul li').click(function () {
          var url = $(this).data("init-url");
          // alert(url);
          if (url) {
            $.ajax({
              url: url,
              type: 'GET',
              dataType: 'json',
              success: function (data) {
                if(data.response == "success") {
                  self.data.set(data);
                }
                self.render();
                self.$el.show();
                popup_element.popover('hide');
              },
              error: function (){
                popup_element.popover('hide');
              }
            });
          }
        });
      });
    },

    TakeIn: function( event ){
      // event.preventDefault();
      // Button clicked, you can access the element that was clicked with event.currentTarget
      var url = this.data.get('take_in_url');
      var self = this;
      if (url) {
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              self.data.set(data);
              self.data.set({take_in_url: null});
            } else if (data.response == "error") {
              alert(data.error);
            }
            self.render();
          },
        });
      }
    },

    Done: function( event ){
      // event.preventDefault();
      var self = this;
      var url = self.data.get('done_url');
      // var form = $(event.currentTarget).parents('form');
      var data = self.$form.serialize();
      if (url) {
        $.ajax({
          url: url,
          data: data,
          type: 'POST',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              self.data.set(data);
              self.data.set({
                active: false,
                status: 3,
                title_translated: self.$form.find('input[name="title_translated"]').val(),
                details_translated: self.$form.find('textarea[name="details_translated"]').val(),
              });
              self.render();
            }
          },
        });
      }
    },

    Take_off: function( event ){
      // event.preventDefault();
      // Button clicked, you can access the element that was clicked with event.currentTarget
      var url = this.data.get('take_off');
      var self = this;
      if (url) {
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            self.data.set({
              active: false,
              status: 0,
              take_in_url: data.take_in_url
            });
            self.render();
          },
        });
      }
    },

    Confirm: function( event ){
      // event.preventDefault();
      // Button clicked, you can access the element that was clicked with event.currentTarget
      var self = this;
      var url = self.data.get('approval_url');
      var data = [];
      if (self.data.get('active') && self.data.get('status') == 3) {
        data = self.$form.serialize();
      }
      if (url) {
        $.ajax({
          url: url,
          data: data,
          type: 'POST',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              location.reload();
            } else if (data.response == "error") {
              alert('Error: something is bad. Please reload the page and try again.');
            }
          },
        });
      }
    },

    Revoke: function( event ){
      // event.preventDefault();
      // Button clicked, you can access the element that was clicked with event.currentTarget
      var url = this.data.get('revoke_url');
      var self = this;
      if (url) {
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              location.reload();
            } else if (data.response == "error") {
              alert('Error: something is bad');
            }
          },
        });
      }
      this.render();
    },

    Correction: function( event ){
      // event.preventDefault();
      // Button clicked, you can access the element that was clicked with event.currentTarget
      var url = this.data.get('correction_url');
      var self = this;
      if (url) {
        $.ajax({
          url: url,
          type: 'POST',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              location.reload();
            } else if (data.response == "error") {
              alert('Error: something is bad');
            }
          },
        });
      }
      this.render();
    },

    Edit: function( event ){
      // event.preventDefault();
      if (this.data.get('active') && confirm('Are you sure you wish to cancel your edit? This translation will revert to it\'s original post.')) {
        this.data.set({active: !this.data.get('active')});
        this.render();
      } else if (!this.data.get('active')) {
        this.data.set({active: !this.data.get('active')});
        this.render();
      }
    },

  });

  global.ahr.initViewPost = function (options) {
    new PostView({el: '.view-post', getCommentsUrl: options.getCommentsUrl, addCommentUrl: options.addCommentUrl, deleteCommentUrl: options.deleteCommentUrl});
  };

  global.ahr.initViewPostTranslation = function (options) {
    new TranslateView(options);
  };

})(window);
