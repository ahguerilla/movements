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
      this.loadComments();

      this.report_widget = new window.ahr.ReportPostView();
      this.linkifyContent();

      this.initTranslatePopup();
      var translate_url = $(".view-post").data('default_translate_url');
      if (translate_url && (this.options.postLanguage != this.options.userDefaultLangage)) {
        this.translate(translate_url);
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
          var url = $(this).data("translate_url");
          if (url) {
            self.translate(url);
          }
          var lang = url.replace('?human=false', '').slice(-3);
          _.each($('.comment'), function (comment) {
            self.translateComment($(comment).data('translate-language-url').slice(0, -3) + lang, $(comment));
          });
          $('.translate span').popover('toggle');
        });
      });
    },

    translate: function(translate_url) {
      var self = this;
      var post = $(".post");
      $.ajax({
        url: translate_url,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          if(data.response === "success") {
            var trans_lang = translate_url.split('lang_code=')[1];
            $('#post-title').text(data.title_translated);
            if (trans_lang === data.source_language){
              post.find('#post-body-translated').text("").hide();
              post.find('div.translated_by').hide();
            } else {
              post.find('#post-body-translated').text(data.details_translated).show();
              if (data.status == 4) {
                post.find('div.translated_by a.user').html(data.username).attr('data-translate_url', translate_url);
                post.find('div.translated_by a.google').attr('data-translate_url', translate_url.replace('?human=false', '') + '?human=false');
                post.find('div.translated_by span').show();
              } else if (!data.human_aviable) {
                post.find('div.translated_by span').hide();
                post.find('div.translated_by a.user').attr('data-translate_url', '');
              }
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
      var url = $(ev.currentTarget).data('translate_url');
      if (url) {
        this.translate(url);
      }
    },

    changeCommentTranslation: function(ev) {
      ev.preventDefault();
      var url = $(ev.currentTarget).data('translate_url');
      var comment = $(ev.currentTarget).parents('div.comment');
      if (url) {
        this.translateComment(url, comment);
      }
    },

    translateComment: function(url, object) {
      $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          if(data.response === "success") {
              var _url = url.replace('?human=false', '');
              if(_url.slice(-3, -1) === data.source_language){
                object.find('#comment-body-translated').text('').hide();
                object.find('div.translated_by').hide();
              } else {
                object.find('#comment-body-translated').text(data.details_translated).show();
                if (data.status == 4) {
                  object.find('div.translated_by a.user').html(data.username).attr('data-translate_url', _url);
                  object.find('div.translated_by a.google').attr('data-translate_url', _url + '?human=false');
                  object.find('div.translated_by span').show();
                } else if (!data.human_aviable) {
                  object.find('div.translated_by span').hide();
                  object.find('div.translated_by a.user').attr('data-translate_url', '');
                }
                object.find('div.translated_by').show();
              }
            } else {
              object.find('#comment-body-translated').text('').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
              object.find('div.translated_by').hide();
            }
          },
        error: function (){
          object.find('#comment-body-translated').text('').html('<p><span style="color:red">Unable to provide translations at this time</span></p>');
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
        // Auto-Google-Translate the post title for each item.
        var comment = $('.comment[comment_id="' + item.pk + '"]');
        if (item.fields.translate_language_url && item.fields.source_lang != item.fields.translate_language_url.slice(-3, -1)) {
          self.translateComment(item.fields.translate_language_url, comment);
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
    },
  });

  var TranslationData = Backbone.Model.extend({
    idAttribute: "id",

    defaults: {
      is_translator: true,
      is_cm: true,
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
      details_translated: '',
      title_translated: '',
      prev_title: null,
      prev_text: null,
      display_title: null,
      display_text: null,
      id: null
    }
  });

  var errorTemplate = _.template(
      '<div class="alert alert-warning">' +
      '  <button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
      '    <span aria-hidden="true">&times;</span>' +
      '  </button><%- message %>' +
      '</div>');

  var TranslateView = Backbone.View.extend({
    el: $('div.view-post'),
    $langaugesPopover: null,
    lang_code: null,

    events: {
        "click a.post-pre-init": "preInit",
        "click div.post-actions div.language-selector li": "TakeIn",
        "click #post-translation-container button#done": "completeTranslation",
        "click #post-translation-container button#take_off": "cancelTranslation",
        "click #post-translation-container button#confirm": "Confirm",
        "click #post-translation-container button#revoke": "Revoke",
        "click #post-translation-container button#edit": "Edit",
        "click #post-translation-container button#correction": "Correction"
    },

    initialize: function(options){
      this.$MenuTemplate = _.template($('#init-languages-menu-template').html());
      this.$areaTemplate = _.template($('#translation-area').html());
      this.$areaContainer = this.$el.find('#post-translation-container');
      this.$PostinitMenuarea = $('div.post-languages-menu');
      this.data = new TranslationData();
      this.data.set(options);
    },

    render: function(){
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

    renderError: function(message) {
      this.$areaContainer.html(errorTemplate({message: message}));
      this.$areaContainer.show();
    },

    preInit: function(ev){
      ev.preventDefault();
      var self = this;
      this.$langaugesPopover = self.$PostinitMenuarea.find('span');
      var container = self.$PostinitMenuarea.find('#post-languages-menu-container');
      if (container.html() == '') {
        this.$langaugesPopover.popover({
          trigger: 'manual',
          title: '',
          html: true,
          content: self.$MenuTemplate(),
          container: container,
          placement: 'top'
        });
      }
      this.$langaugesPopover.popover('toggle');
    },

    TakeIn: function(event) {
      var $currentTarget = $(event.currentTarget);
      this.lang_code = $currentTarget.data('lang-code');
      this.data.set({'lang_code': this.lang_code});
      $.ajax({
        url: this.$el.data('takein-url'),
        context: this,
        data: {
          lang_code: this.lang_code
        },
        type: 'post',
        dataType: 'json',
        success: function (data) {
          if(data.response == "success") {
            this.data.set(data);
            this.render();
          } else if (data.response == "error") {
            this.renderError(data.error);
          }
        }
      });
      this.$langaugesPopover.popover('toggle');
    },

    completeTranslation: function(event){
      var self = this;
      var url = self.data.get('done_url');
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
          }
        });
      }
    },

    cancelTranslation: function( event ){
      var url = this.data.get('take_off');
      var self = this;
      if (url) {
        $.ajax({
          url: url,
          type: 'post',
          data: {
            lang_code: this.lang_code
          },
          dataType: 'json',
          success: function (data) {
            self.data.set({
              active: false,
              status: 0
            });
            self.render();
          }
        });
      }
    },

    Confirm: function(event) {
      var self = this;
      var data = [];
      if (self.data.get('active') && self.data.get('status') == 3) {
        data = self.$form.serialize();
      } else {
        data = {
          lang_code: this.lang_code
        }
      }
      $.ajax({
        url: self.data.get('approval_url'),
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

    Revoke: function(ev) {
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

    Edit: function( event ){
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
        "click div.comment div.language-selector li": "Init",
        "click div.comment button#take_in": "TakeIn",
        "click div.comment button#done": "completeTranslation",
        "click div.comment button#take_off": "cancelTranslation",
        "click div.comment button#confirm": "Confirm",
        "click div.comment button#revoke": "Revoke",
        "click div.comment button#edit": "Edit",
        "click div.comment button#correction": "Correction",
    },

    getComment: function(ev){
      this.comment = $(ev.currentTarget).parents('div.comment');
      this.comment_id = this.comment.attr('comment_id');
      this.comment_data = this.dataStorage.get(this.comment_id);
      this.$form = this.comment.find('form');
    },

    preInit: function(ev){
      ev.preventDefault();
      this.getComment(ev);
      var self = this;
      var popup_element = self.comment.find('div.comment-languages-menu span');
      if (self.comment.find('#comment-languages-menu-container').html() == '') {
        $.ajax({
          url: $(ev.currentTarget).attr('href'),
          data: {'object_id': self.comment_id},
          type: 'POST',
          dataType: 'json',
          success: function (data) {
            var menu = self.$MenuTemplate(data)
            popup_element.popover({
              trigger: 'manual',
              title: '',
              html: true,
              content: menu,
              container: self.comment.find('#comment-languages-menu-container'),
              placement: 'top'
            });
            popup_element.popover('show');
          },
        });
      } else {
        popup_element.popover('toggle')
      }
    },

    Init: function(ev) {
      this.getComment(ev);
      this.comment.find('div.comment-languages-menu span').popover('toggle'); // toggle popover
      var self = this;
      $.ajax({
        url: $(ev.currentTarget).data('api-url'),
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          if (data.response == 'success') {
            self.dataStorage.set(data);
            self.render(self.comment_id);
          } else {
            alert('Failed to fetch translation record. The object DoesNotExist or DB is to busy.');
          }
        },
        error: function () {
            alert('Failed to fetch record. The object DoesNotExist or DB is to busy.');
        }
      });

    },

    initialize: function(options){
      this.$MenuTemplate = _.template($('#init-languages-menu-template').html());
      this.$areaTemplate = _.template($('#comment-translation-area').html());
      var collection = Backbone.Collection.extend({model: TranslationData});
      this.dataStorage = new collection;
    },

    render: function(comment_id){
      this.comment = $('div.comment[comment_id="' + comment_id + '"]');
      this.comment_id = comment_id
      this.comment_data = this.dataStorage.get(this.comment_id);
      if (this.comment_data.get('status') == 3) {
        var diff = JsDiff.diffChars(this.comment_data.get('prev_text'), this.comment_data.get('details_translated'));
        var display_text= '';
        diff.forEach(function(part){
          var color = part.added ? 'green' :
            part.removed ? 'red' : 'grey';
          display_text += '<span style="color:' + color + ';">' + part.value + '</span>'
        });
        this.comment_data.set('display_text', display_text);
        this.dataStorage.set(this.comment_data);
      }
      this.comment.find('#comment-translation-container').html( this.$areaTemplate(this.comment_data.attributes) ).show();
    },

    TakeIn: function(ev){
      this.getComment(ev);
      var url = this.comment_data.get('take_in_url');
      var self = this;
      if (url) {
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              self.comment_data.set(data);
              self.comment_data.set({take_in_url: null});
              self.dataStorage.set(self.comment_data);
            } else if (data.response == "error") {
              alert(data.error);
            }
            self.render(self.comment_id);
          }
        });
      }
    },

    completeTranslation: function(ev){
      this.getComment(ev);
      var self = this;
      var url = self.comment_data.get('done_url');
      if (url) {
        $.ajax({
          url: url,
          data: self.$form.serialize(),
          type: 'POST',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              self.comment_data.set(data);
              self.comment_data.set({
                active: false,
                status: 3,
                details_translated: self.$form.find('textarea[name="details_translated"]').val()
              });
              self.dataStorage.set(self.comment_data);
              self.render(self.comment_id);
            } else {
              alert(data.error);
            }
          }
        });
      }
    },

    cancelTranslation: function(ev){
      this.getComment(ev);
      var self = this;
      var url = self.comment_data.get('take_off');
      if (url) {
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            if (data.response == 'success') {
              self.comment_data.set({
                active: false,
                status: 0,
                take_in_url: data.take_in_url
              });
              self.render(self.comment_id);
              } else {
                alert(data.error);
              }
          }
        });
      }
    },

    Confirm: function(ev){
      this.getComment(ev);
      var url = this.comment_data.get('approval_url');
      var data = [];
      if (this.comment_data.get('active') && this.comment_data.get('status') == 3) {
        data = this.$form.serialize();
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
            } else {
              alert(data.error);
            }
          },
        });
      }
    },

    Edit: function(ev){
      this.getComment(ev);
      var active = this.comment_data.get('active');
      if (active && confirm('Are you sure you wish to cancel your edit? This translation will revert to it\'s original post.')) {
        this.comment_data.set({active: !active});
      } else if (!active) {
        this.comment_data.set({active: !active});
      }
      this.dataStorage.set(this.comment_data);
      this.render(this.comment_id);
    },

    Revoke: function(ev){
      this.getComment(ev);
      var url = this.comment_data.get('revoke_url');
      if (url) {
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              location.reload();
            } else {
              alert(data.error);
            }
          },
        });
      }
    },

    Correction: function(ev){
      this.getComment(ev);
      var url = this.comment_data.get('correction_url');
      if (url) {
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            if(data.response == "success") {
              location.reload();
            } else {
              alert(data.error);
            }
          },
        });
      }
    },

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
