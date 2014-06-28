(function () {
  var UserSettingsView = Backbone.View.extend({
    el: 'body',
    events:{
      'click #changeavatar': 'ShowAvChange',
      'click #changepassword' : 'ShowChangePass',
      'click .select-checkbox': 'checkClick',
    },

    showPersonal: function(ev) {
      $('#personal-tab').show();
      $('#personal-select').addClass("selected");
      $('#skills-tab').hide();
      $('#skills-select').removeClass("selected");
      $('#security-tab').hide();
      $('#security-select').removeClass("selected");
    },

    showSkills: function(ev) {
      $('#personal-tab').hide();
      $('#personal-select').removeClass("selected");
      $('#skills-tab').show();
      $('#skills-select').addClass("selected");
      $('#security-tab').hide();
      $('#security-select').removeClass("selected");
    },

    showSecurity: function(ev){
      $('#personal-tab').hide();
      $('#personal-select').removeClass("selected");
      $('#skills-tab').hide();
      $('#skills-select').removeClass("selected");
      $('#security-tab').show();
      $('#security-select').addClass("selected");
    },

    checkClick: function(ev){
      $(ev.currentTarget).find('input[type="checkbox"]').prop("checked", !$(ev.currentTarget).find('input[type="checkbox"]').prop("checked"));
      $(ev.currentTarget).toggleClass("checked");
      if( $(ev.currentTarget).closest('.select-multi-items') ){
        this.updateCounts();
      }
    },

    ShowChangePass:function(ev){
      ev.preventDefault();
      var form_class = $(ev.currentTarget).attr('form_class');
      var that = this;
      var dfrd = $.ajax({url:ev.currentTarget.href});
      dfrd.done(function(data){
        $('#profile_change_password').html($('form.'+form_class, data).parent().html());
        var func = _.bind(that.changepassword,that);
        $('#changepasswordbutton').on('click',func);
      });
      $('#changepassworddialog').modal('show');
      return false;
    },

    ShowAvChange: function(ev){
      ev.preventDefault();
      $('#avataralert').empty();
      var that = this;
      var href = document.getElementById('changeavatar').href;
      var dfrd = $.ajax({url:href});
      dfrd.done(function(data){
        $('#profile_change_stuff').html($('form',data).parent().parent().html());
        if($('#avatarchangeimage').length>0){
          var func = _.bind(that.changeavatar,that);
          $('#avatarchangeimage').on('click',func);
        }
        var func = _.bind(that.uploadnewimage,that);
        $('#avatarnewimageupload').on('click',func);
        $('#changeavatardialog').modal('show');
      });
      return(false);
    },

    changeavatar:function(ev){
      ev.preventDefault();
      var href = $('form','#profile_change_stuff')[0].action;
      var dfrd = $.ajax({
        url:href,
        type: 'post',
        data:$($('form','#profile_change_stuff')[0]).serialize()
      });
      dfrd.done(function(data){
        $('#changeavatardialog').modal('hide');
      });
      return false;
    },

    uploadnewimage:function(ev){
      ev.preventDefault();
      formdata = new FormData();
      var fileinp = $('input[type=file]', $('#changeavatardialog'));
      if(fileinp[0].value==""){
        return false;
      }


      var file = fileinp[0].files[0];
      if (!file.type.match(/image.*/)){
        window.ahr.alert('{%trans "The file you selected is not an image"%}','#avataralert');
        return false;
      }
      var reader = new window.FileReader();
      reader.readAsDataURL(file);
      formdata.append('avatar', file);
      var token = $('input[name="csrfmiddlewaretoken"]',$(ev.currentTarget).closest('form')).val()
      formdata.append('csrfmiddlewaretoken',token);
      $('label[for="id_avatar"]').text('Uploading  ');
      //$('input[type=file]', $('#changeavatardialog')).replaceWith('<img style="border-radius:0%;" src="{{ STATIC_URL}}images/download.gif" />');
      var dfrd = $.ajax({
        url:$(ev.currentTarget).closest('form').attr('action'),
        data: formdata,
        processData: false,
        contentType: false,
        type: 'post'
      });
      dfrd.done(function(data){
        $('#changeavatardialog').modal('hide');
      });

      return false;
    },

    changepassword: function(ev){
      ev.preventDefault();
      var that = this;
      var form = $(ev.currentTarget).closest('form');

      var aurl = window.ahr.app_urls.changepassword,
        form_class= 'password_change';

      if ($($(ev.currentTarget).closest('form')).hasClass('password_set')){
        aurl = window.ahr.app_urls.setpassword;
        form_class= 'password_set';
      }

      var dfrd = $.ajax({
        url:aurl,
        type: 'post',
        data: form.serialize()
        });

      dfrd.done(function(data){
        $('#changepasswordbutton').off('click');
        if($('form.'+form_class, data).length==0){
          $('#changepassworddialog').modal('hide');
          if(form_class=='password_set'){
            $('#changepassword').attr('href', window.ahr.app_urls.changepassword);
            $('#changepassword').attr('form_class', 'password_change');
            $('#changepassword').text('{%trans "Change password"%}');
          }
          return false;
        }
        $('#profile_change_password').html($('form.'+form_class, data).parent().html());
        var func = _.bind(that.changepassword, that);
        $('#changepasswordbutton').on('click', func);
      });
      return false;
    },

    initialize : function(){
      $('#changeavatardialog').on('hidden.bs.modal', function () {
        $('#profile_change_stuff').empty();
        var href = document.getElementById('changeavatar').href;
        $('#profile_change_stuff').attr('src', href);
        var dfrd = $.ajax({
          url : window.ahr.app_urls.getavatar.replace(0,window.ahr.user_id)+'80'
        });
        dfrd.done(function(data){
          $('#settingavatar>img').attr('src',data.avatar+'?' + new Date().getTime());
        });
        var dfrd2 = $.ajax({
          url : window.ahr.app_urls.getavatar.replace(0,window.ahr.user_id)+'50'
        });
        dfrd2.done(function(data){
          $('.navavatar img').attr('src',data.avatar+'?' + new Date().getTime());
        });
      });
      return this;
    }
  });

  var SettingsRouter = Backbone.Router.extend({
    userSettingsView: null,
    routes: {
      "": "showDefault",
      "personal": "showPersonal",
      "skills": "showSkills",
      "security": "showSecurity"
    },
    initialize: function (options) {
      this.userSettingsView = options.userSettingsView;
    },
    showDefault: function() {
      this.userSettingsView.showPersonal();
    },
    showPersonal: function() {
      this.userSettingsView.showPersonal();
    },
    showSkills: function() {
      this.userSettingsView.showSkills();
    },
    showSecurity: function() {
      this.userSettingsView.showSecurity();
    }
  });

  window.ahr = window.ahr || {};
  window.ahr.widgets = window.ahr.widgets || {};
  window.ahr.widgets.initUserSettingsView = function () {
    var widget = new UserSettingsView();
    var options = {
      userSettingsView: widget
    };
    var router = new SettingsRouter(options);
    Backbone.history.start()
  };
})();