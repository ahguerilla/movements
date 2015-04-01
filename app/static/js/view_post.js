(function (global) {

  var PostView = Backbone.View.extend({
    events: {
      'submit .comments form': 'submitComment',
      'click .report': 'showReportForm',
      'click .delete-comment': 'deleteComment',
      'click .tweet': 'shareTwitter',
      'click div.post .translated_by a': 'changePostTranslation',
      'click div.comment-body .translated_by a': 'changeCommentTranslation'
    },

    initialize: function(options) {
      this.options = options;
      this.$commentsLoading = this.$el.find('.comment-list .loader');
      this.$commentListContent = this.$el.find('.comment-list .content');
      this.$commentTemplate = _.template($('#comment-template').html());
      this.$commentText = this.$el.find('.comments form textarea');
      this.$submitButton = this.$el.find('.comments form button');
      this.translatedByTemplate = _.template($('#translated-by-template').html());
      this.loadComments();

      this.report_widget = new window.ahr.ReportPostView();
      this.linkifyContent();

      this.initTranslatePopup();
      var translate_url = $(".view-post").data('default_translate_url');
      this.currentLanguage = this.options.userDefaultLangage;
      if (translate_url && (this.options.postLanguage != this.options.userDefaultLangage)) {
        this.translate(translate_url, true);
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
        $('#translate-menu-container .language-selector ul li').click(function () {
          self.translate($(this).data("translate_url"), true);
          _.each($('.comment'), function (comment) {
            var commentTranslateUrl = $(comment).data('translate-language-url') + '?lang_code=' + self.currentLanguage;
            self.translateComment(commentTranslateUrl, $(comment), true);
          });
          $('.translate span').popover('toggle');
        });
      });
    },

    translate: function(translate_url, human) {
      var self = this;
      var post = $(".post");
      var trans_lang = translate_url.split('lang_code=')[1];
      this.currentLanguage = trans_lang;

      var actualUrl = translate_url;
      if (!human) {
        if (translate_url.indexOf('?') > 0) {
          actualUrl = translate_url + '&human=false';
        } else {
          actualUrl = translate_url + '?human=false';
        }
      }

      $.ajax({
        url: actualUrl,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          if(data.response === "success") {
            $('#post-title').text(data.title_translated);
            if (trans_lang === data.source_language){
              post.find('#post-body-translated').text("").hide();
              post.find('div.translated_by').hide();
            } else {
              post.find('#post-body-translated').text(data.details_translated).show();
              post.find('div.translated_by')
                  .html(self.translatedByTemplate({
                    humanTranslation: data.status == 4,
                    humanAvailable: data.human_aviable,
                    translateUrl: translate_url,
                    username: data.human_translator
                  }))
                  .show();
              post.find('div.translated_by').show();
            }
            self.linkifyContent();
          } else {
            post.find('#post-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>').show();
          }
        },
        error: function (){
          post.find('#post-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>').show();
        }
      });
    },

    changePostTranslation: function(ev) {
      ev.preventDefault();
      var $currentTarget = $(ev.currentTarget);
      this.translate($currentTarget.data('translate_url'), $currentTarget.data('human'));
    },

    changeCommentTranslation: function(ev) {
      ev.preventDefault();
      var comment = $(ev.currentTarget).parents('div.comment');
      var translateUrl = comment.data('translate-language-url');
      translateUrl += '?lang_code=' + this.currentLanguage;
      this.translateComment(translateUrl, comment, $(ev.currentTarget).data('human'));
    },

    translateComment: function(url, object, human) {
      var self = this;
      var actualUrl = url;
      if (!human) {
        if (url.indexOf('?') > 0) {
          actualUrl = url + '&human=false';
        } else {
          actualUrl = url + '?human=false';
        }
      }

      $.ajax({
        url: actualUrl,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          if(data.response === "success") {
              if(data.source_language === data.lang_code){
                object.find('#comment-body-translated').text('').hide();
                object.find('div.translated_by').hide();
              } else {
                object.find('#comment-body-translated').text(data.details_translated).show();
                object.find('div.translated_by')
                      .html(self.translatedByTemplate({
                        humanTranslation: data.status == 4,
                        humanAvailable: data.human_aviable,
                        translateUrl: url,
                        username: data.human_translator
                      }))
                      .show();
              }
            } else {
              object.find('#comment-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
              object.find('div.translated_by').hide();
            }
          },
        error: function (){
          object.find('#comment-body-translated').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
          object.find('div.translated_by').hide();
        }
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
      var self = this;
      self.$commentListContent.html('');
      _.each(comments, function(item) {
        var comment_html = self.$commentTemplate(item.fields);
        self.$commentListContent.append(comment_html);

        var comment = $('.comment[comment_id="' + item.pk + '"]');
        if (item.fields.translate_language_url && (item.fields.source_lang != self.currentLanguage)) {
          self.translateComment(item.fields.translate_language_url, comment, true);
        }
      });
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

  var TranslationData = Backbone.Model.extend({
    idAttribute: "id",

    defaults: {
      is_translator: true,
      is_cm: false,
      active: false,
      lang_code: '',
      status: null,
      correction: false,
      take_in_url: null,
      take_off: null,
      mark_done: null,
      approval_url: null,
      revoke_url: null,
      correction_url: null,
      put_back_to_edit_url: null,
      save_draft_url: null,
      details_translated: '',
      title_translated: '',
      prev_title: null,
      prev_text: null,
      display_title: null,
      display_text: null,
      other_user_editing: false,
      error: '',
      message: '',
      user_is_owner: false,
      id: null
    }
  });

  var TranslateView = Backbone.View.extend({
    el: $('div.view-post'),
    $langaugesPopover: null,
    lang_code: null,

    events: {
        "click a.post-pre-init": "preInit",
        "click div.post-actions div.language-selector li": "TakeIn",
        "click #post-translation-container button#save_draft": "saveDraft",
        "click #post-translation-container button#done": "completeTranslation",
        "click #post-translation-container button#take_off": "cancelTranslation",
        "click #post-translation-container a.back-to-edit": "backToEdit",
        "click #post-translation-container button#confirm": "Confirm",
        "click #post-translation-container button#revoke": "Revoke",
        "click #post-translation-container button#edit": "Edit",
        "click #post-translation-container button#correction": "Correction",
        "click #post-translation-container #take_over": 'takeOver',
        "click #post-translation-container #cancel_take_over": 'cancelTakeOver'
    },

    initialize: function(options){
      this.$MenuTemplate = _.template($('#init-languages-menu-template').html());
      this.$areaTemplate = _.template($('#translation-area').html());
      this.$areaContainer = this.$el.find('#post-translation-container');
      this.$PostinitMenuarea = $('div.post-languages-menu');
      this.translationLanguages = options.translationLanguages;
      this.postLanguage = options.postLanguage;
      this.data = new TranslationData();
      this.data.set(options);
    },

    clearMessages: function() {
      this.data.set({'error': null, 'message': null});
    },

    render: function() {
      var self = this;
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
        diff = JsDiff.diffChars(self.data.get('prev_text'), self.data.get('details_translated'));
        var display_text= '';
        diff.forEach(function(part){
          var color = part.added ? 'green' :
            part.removed ? 'red' : 'grey';
          display_text += '<span style="color:' + color + ';">' + part.value + '</span>'
        });
        self.data.set('display_text', display_text);
      }
      this.$areaContainer.html(this.$areaTemplate(this.data.attributes));
      this.$areaContainer.show();
      this.$form = this.$areaContainer.find('form');
    },

    preInit: function(ev) {
      ev.preventDefault();
      var self = this;
      this.$langaugesPopover = self.$PostinitMenuarea.find('span');
      var container = self.$PostinitMenuarea.find('#post-languages-menu-container');
      if (container.html() == '') {
        this.$langaugesPopover.popover({
          trigger: 'manual',
          title: '',
          html: true,
          content: self.$MenuTemplate({languages: this.translationLanguages, itemLanguage: this.postLanguage}),
          container: container,
          placement: 'top'
        });
      }
      this.$langaugesPopover.popover('toggle');
    },

    TakeIn: function(event, force) {
      if (event) {
        var $currentTarget = $(event.currentTarget);
        this.lang_code = $currentTarget.data('lang-code');
        this.data.set({'lang_code': this.lang_code});
      }
      var data = {
        lang_code: this.lang_code
      };
      if (force) {
        data['force'] = '1';
      }
      $.ajax({
        url: this.$el.data('takein-url'),
        context: this,
        data: data,
        type: 'post',
        dataType: 'json',
        success: function (data) {
          this.clearMessages();
          this.data.set(data);
          this.render();
        }
      });
      if (event) this.$langaugesPopover.popover('toggle');
    },

    takeOver: function () {
      this.TakeIn(null, true);
    },

    cancelTakeOver: function() {
      this.$areaContainer.hide();
    },

    saveDraft: function() {
      $.ajax({
        url: this.data.get('save_draft_url'),
        context: this,
        data: this.$form.serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          this.clearMessages();
          this.data.set(data);
          this.render();
        }
      });
    },

    completeTranslation: function() {
      $.ajax({
        url: this.data.get('done_url'),
        context: this,
        data: this.$form.serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          this.clearMessages();
          this.data.set(data);
          if (data.response == "success") {
            this.data.set({
              active: false,
              status: 3,
              title_translated: this.$form.find('input[name="title_translated"]').val(),
              details_translated: this.$form.find('textarea[name="details_translated"]').val()
            });
          }
          this.render();
        }
      });
    },

    backToEdit: function(event) {
      event.preventDefault();
      $.ajax({
        url: this.data.get('put_back_to_edit_url'),
        context: this,
        data: {
          lang_code: this.lang_code
        },
        type: 'post',
        dataType: 'json',
        success: function (data) {
          this.clearMessages();
          this.data.set(data);
          this.render();
        }
      });
    },

    cancelTranslation: function() {
      $.ajax({
        context: this,
        url: this.data.get('take_off'),
        type: 'post',
        data: {
          lang_code: this.lang_code
        },
        dataType: 'json',
        success: function () {
          this.clearMessages();
          this.data.set({
            active: false,
            status: 0
          });
          this.render();
        }
      });
    },

    Confirm: function() {
      var data = [];
      if (this.data.get('active') && this.data.get('status') == 3) {
        data = this.$form.serialize();
      } else {
        data = {
          lang_code: this.lang_code
        }
      }
      $.ajax({
        context: this,
        url: this.data.get('approval_url'),
        data: data,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          if(data.response == "success") {
            location.reload();
          } else {
            alert(data.error);
          }
        }
      });
    },

    Revoke: function() {
      $.ajax({
        url: this.data.get('revoke_url'),
        type: 'post',
        data: {lang_code: this.lang_code},
        dataType: 'json',
        success: function (data) {
          if(data.response == "success") {
            location.reload();
          } else if (data.response == "error") {
            console.log(data);
          }
        }
      });
    },

    Correction: function(ev) {
      $.ajax({
        url: this.data.get('correction_url'),
        type: 'post',
        data: {lang_code: this.lang_code},
        dataType: 'json',
        success: function (data) {
          if(data.response == "success") {
            location.reload();
          } else if (data.response == "error") {
            console.log(data);
          }
        }
      });
    },

    Edit: function() {
      if (this.data.get('active') && confirm('Are you sure you wish to cancel your edit? This translation will revert to it\'s original post.')) {
        this.data.set({active: !this.data.get('active')});
        this.render();
      } else if (!this.data.get('active')) {
        this.data.set({active: !this.data.get('active')});
        this.render();
      }
    }
  });

  var CommentsTranslationView = Backbone.View.extend({
    el: $('div.comment-list'),

    events: {
        "click a.comment-pre-init": "preInit",
        "click div.comment div.language-selector li": "TakeIn",
        "click div.comment  button#save_draft": "saveDraft",
        "click div.comment button#done": "completeTranslation",
        "click div.comment button#take_off": "cancelTranslation",
        "click div.comment  a.back-to-edit": "backToEdit",
        "click div.comment button#confirm": "Confirm",
        "click div.comment button#revoke": "Revoke",
        "click div.comment button#edit": "Edit",
        "click div.comment button#correction": "Correction",
        "click div.comment #take_over": 'takeOver',
        "click div.comment #cancel_take_over": 'cancelTakeOver'
    },

    getComment: function(ev){
      this.comment = $(ev.currentTarget).parents('div.comment');
      this.comment_id = this.comment.attr('comment_id');
      this.$form = this.comment.find('form');
      var data = this.commentDataCache[this.comment_id];
      if (!data) {
        data = new TranslationData();
        data.set('lang_code', this.comment.data('language'));
        this.commentDataCache[this.comment_id] = data;
      }
      this.data = data;
      this.data.set({'error': null, 'message': null});
    },

    initialize: function (options) {
      this.$MenuTemplate = _.template($('#init-languages-menu-template').html());
      this.$areaTemplate = _.template($('#comment-translation-area').html());
      this.options = options;
      this.translationLanguages = options.translationLanguages;
      this.commentDataCache = {};
    },

    render: function () {
      this.comment = $('div.comment[comment_id="' + this.comment_id + '"]');
      this.comment_id = this.comment_id;
      if (this.data.get('status') == 3) {
        var diff = JsDiff.diffChars(this.data.get('prev_text'), this.data.get('details_translated'));
        var display_text = '';
        diff.forEach(function (part) {
          var color = part.added ? 'green' :
              part.removed ? 'red' : 'grey';
          display_text += '<span style="color:' + color + ';">' + part.value + '</span>'
        });
        this.data.set('display_text', display_text);
      }
      this.comment.find('#comment-translation-container')
          .html(this.$areaTemplate(this.data.attributes))
          .show();
    },

    preInit: function(ev) {
      ev.preventDefault();
      this.getComment(ev);
      var self = this;
      var popup_element = self.comment.find('div.comment-languages-menu span');
      if (self.comment.find('#comment-languages-menu-container').html() == '') {
        popup_element.popover({
          trigger: 'manual',
          title: '',
          html: true,
          content: self.$MenuTemplate({languages: this.translationLanguages, itemLanguage: this.data.get('lang_code')}),
          container: self.comment.find('#comment-languages-menu-container'),
          placement: 'top'
        });
      }
      popup_element.popover('toggle');
    },

    TakeIn: function(ev, force){
      if (ev) {
        this.getComment(ev);
        this.data.set(this.options);
        var $currentTarget = $(ev.currentTarget);
        this.data.set({'lang_code': $currentTarget.data('lang-code')});
      }

      var data = {
        lang_code: this.data.get('lang_code')
      };

      if (force) {
        data['force'] = '1';
      }

      var self = this;
      $.ajax({
        url: this.comment.data('take-in-url'),
        data: data,
        type: 'post',
        dataType: 'json',
        success: function (data) {
          self.data.set(data);
          self.render();
        }
      });

      if (ev) {
        var popup_element = self.comment.find('div.comment-languages-menu span');
        popup_element.popover('toggle');
      }
    },

    takeOver: function (ev) {
      this.getComment(ev);
      this.TakeIn(null, true);
    },

    cancelTakeOver: function (ev) {
      this.getComment(ev);
      this.comment.find('#comment-translation-container')
          .hide();
    },

    saveDraft: function (ev) {
      this.getComment(ev);
      $.ajax({
        url: this.data.get('save_draft_url'),
        context: this,
        data: this.$form.serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          this.data.set(data);
          this.render();
        }
      });
    },

    completeTranslation: function(ev){
      this.getComment(ev);
      var self = this;
      $.ajax({
        url: self.data.get('done_url'),
        data: self.$form.serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          self.data.set(data);
          if (data.response == "success") {
            self.data.set({
              active: false,
              status: 3,
              details_translated: self.$form.find('textarea[name="details_translated"]').val()
            });
          }
          self.render();
        }
      });
    },

    backToEdit: function (ev) {
      this.getComment(ev);
      ev.preventDefault();
      $.ajax({
        url: this.data.get('put_back_to_edit_url'),
        context: this,
        data: {
          lang_code: this.data.get('lang_code')
        },
        type: 'post',
        dataType: 'json',
        success: function (data) {
          this.data.set(data);
          this.render();
        }
      });
    },

    cancelTranslation: function(ev){
      this.getComment(ev);
      var self = this;
      $.ajax({
        url: self.data.get('take_off'),
        type: 'post',
        data: {
          lang_code: this.data.get('lang_code')
        },
        dataType: 'json',
        success: function (data) {
          self.data.set({
            active: false,
            status: 0,
            take_in_url: data.take_in_url
          });
          self.render();
        }
      });
    },

    Confirm: function(ev){
      this.getComment(ev);
      var data = [];
      if (this.data.get('active') && this.data.get('status') == 3) {
        data = this.$form.serialize();
      } else {
        data = {
          lang_code: this.data.get('lang_code')
        }
      }
      $.ajax({
        url: this.data.get('approval_url'),
        data: data,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          if(data.response == "success") {
            location.reload();
          } else {
            console.log(data);
          }
        }
      });
    },

    Edit: function(ev){
      this.getComment(ev);
      var active = this.data.get('active');
      if (active && confirm('Are you sure you wish to cancel your edit? This translation will revert to it\'s original post.')) {
        this.data.set({active: !active});
      } else if (!active) {
        this.data.set({active: !active});
      }
      this.render();
    },

    Revoke: function(ev){
      this.getComment(ev);
      $.ajax({
        url: this.data.get('revoke_url'),
        type: 'post',
        data: {lang_code: this.data.get('lang_code')},
        dataType: 'json',
        success: function (data) {
          if(data.response == "success") {
            location.reload();
          } else {
            console.log(data);
          }
        }
      });
    },

    Correction: function(ev) {
      this.getComment(ev);
      $.ajax({
        url: this.data.get('correction_url'),
        type: 'post',
        data: {lang_code: this.data.get('lang_code')},
        dataType: 'json',
        success: function (data) {
          if(data.response == "success") {
            location.reload();
          } else {
            console.log(data);
          }
        }
      });
    }
  });


  global.ahr.initViewPost = function (options) {
    new PostView({
      el: '.view-post',
      getCommentsUrl: options.getCommentsUrl,
      addCommentUrl: options.addCommentUrl,
      deleteCommentUrl: options.deleteCommentUrl,
      postLanguage: options.postLanguage,
      userDefaultLangage: options.userDefaultLangage
    });
  };

  global.ahr.initViewPostTranslation = function (options) {
    new TranslateView(options);
  };

  global.ahr.initCommentTranslationView = function (options) {
    new CommentsTranslationView(options);
  };

})(window);
