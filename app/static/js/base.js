(function(){

  if (ahr.user_id) {
    setInterval(function(){
      var text;
      $.getJSON(window.ahr.app_urls.getmessagecount,function(data){
        $('.message-counter').each(function(tmp,item){
          if(data>0){
             $('#msgcntr',$(item)).text('('+data+')');
          }else{
            $('#msgcntr',$(item)).text('');
          }
        });
      });
    },30000);
  }

  window.ahr.BaseView = Backbone.View.extend({
    events:{},
    showModalDialog: function(templateId, templateData, dialogId, callback) {
      var tmpl = _.template($(templateId).html());
      var tmpl_html = tmpl(templateData);
      $('#modal-placeholder').html(tmpl_html);
      $(dialogId).modal('show');
      if(callback){
        $(dialogId).on('shown.bs.modal', callback);
      }
    },

    invert: function (obj) {
      var new_obj = {};
      for (var prop in obj) {
        if(obj.hasOwnProperty(prop)) {
          new_obj[obj[prop]] = prop;
        }
      }
      return new_obj;
    },

    alert: function(message,selector){
      window.ahr.alert(message,selector);
    },

    info: function (message,selector){
      $(selector).empty();
      $(selector).prepend('<div class="alert alert-success alert-dismissable">'+
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
        message+'</div>');
    }
  });
})();

