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
      'click #backtofolder': 'back',
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
        var more = $('.next',$(data))[0];
        $('.next').replaceWith(more);
        $(more).html('<button style="margin-top:5px;" class="btn btn-default">more...</button>');
        $('.messagelist').append($('.messagelist', $(data)).children());        
      });
    },

    reply: function (ev) {
      ev.reventDefault();
      return false;
    },

    openConv: function (ev) {      
      var subject = $('.subject',$(ev.currentTarget)).children();
      if(subject.is('strong')){
        subject.replaceWith(subject.text());
      }
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
          return "<a href='/market/#item/" + item_id + "'>Click here to view the recommendation</a>";
        });
        data4 = data3.replace(that.userre, function (match, username, offset, string) {
          return "<a href='" + window.ahr.app_urls.viewuserprofile + username + "'>Click here to view the recommendation</a>";
        });
        
        var user;
        $('.messageavatar img', data4).each(function(item,index){
          user = $(this).attr('alt');          
          if(user != window.ahr.username)return false;          
        });  
        if(user == window.ahr.username){
          user = $('.pm_recipient',data4).text();          
        }        
        
        $.getJSON(window.ahr.app_urls.getprofile+user,function(data){
          var tmpl = $('#message-profile').html();
          var prof = _.template(tmpl);
          $('.profilecontainer').html(prof(data));
          $('.rateit').rateit();
          $('.rateit').rateit('min', 0);
          $('.rateit').rateit('max', 5);
          $('.rateit').rateit('readonly', true);
          $('.rateit').each(function(){
            $(this).rateit('value', this.getAttribute('rate'));
          });
          $('#id_body').trigger('focus');                            
        });
                
        $('#conversation').html(data4);
        if($('#id_body').length >0){
          $('#id_body').empty();         
          window.ahr.expandTextarea('#id_body');
        }
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
      if ($(window).width() < 992 ) {
        $('.nanamorde-mobile').show();
      } else if ($(window).width() >= 992) {
        $('.nanamorde').show(); 
      }
      $("#message-col").hide();            
      $('#conversation-cont').show();
      $('#messagenav').hide();
      $('#back').show();
      $('#breadsubject').text($('#messagesubjectheader').text());
      $('body').scrollTop(0);      
    },

    back: function (ev) {
      $('.nanamorde').hide();
      $('.nanamorde-mobile').hide();
      $('#conversation-cont').hide();
      $("#message-col").show();
      $('#back').hide();
      $('#messagenav').show();
    },

    resize: function (ev) {
      if ($(window).width() < 992 && $('#conversation-cont').css('display') != 'none' && $("#message-col").css('display') == 'none') {        
        $('.nanamorde-mobile').show();
        $('.nanamorde').hide();
      } else if ($(window).width() >= 992 && $('#conversation-cont').css('display') != 'none' && $("#message-col").css('display') == 'none') {
        $('.nanamorde-mobile').hide();
        $('.nanamorde').show();
      }else{
        $('.nanamorde-mobile').hide();
        $('#conversation-cont').hide();
      }
    },

    initialize: function () {
      $(window).resize(this.resize);
      this.reportUserWidget = window.ahr.reportUserDialog.initWidget('body');      
      this.itemre = new RegExp(/&lt;!--item=&quot;(\d+)&quot;--&gt;/);
      this.userre = new RegExp(/&lt;!--user=&quot;(\S+)&quot;--&gt;/);
      var more = $('.next')[0];
      $(more).html('<button style="margin-top:5px;" class="btn btn-default">more...</button>');
      $('#paginationblock').html(more);
      $('#conversation-cont').hide();
      $('.nanamorde').hide();
      $('.nanamorde-mobile').hide();
      this.resize();
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.messages = window.ahr.messages || {};
  window.ahr.messages.initInbox = function () {
    var messages = new InboxView();
    var messages_route = new InboxRoute(messages);   
    $('#back').hide();
    Backbone.history.start();
  };
})();