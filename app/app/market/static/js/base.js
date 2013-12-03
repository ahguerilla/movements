(function(){
    setInterval(function(){
        $.getJSON(window.ahr.app_urls.getmessagecount,function(data){
            $('.message-counter').each(function(tmp,item){
                var text = $(item).text()
                var ind = text.indexOf('(');
                var txt = text.slice(0,ind+1);
                if(ind>-1){
                    $(item).text(txt+data+")");
                }
            });
        });
    }
    ,30000);    
})();

window.ahr= window.ahr || {};
window.ahr.BaseView = Backbone.View.extend({
    events:{
        'click .sendprivatemessageuser': 'showpMessage',
        'click .sendpm': 'sendpm',
        'click .cancelpm': 'cancelpm',
        'click .rateuser': 'showRateuser',
        'click .sendurate': 'setrate',
        'click .cancelrate': 'resetrate'
    },
    
    alert: function(message,selector){
	$(selector).empty();
	$(selector).prepend('<div class="alert alert-warning alert-dismissable">'+
	'<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
	message+'</div>');
    },
    
    info: function (message,selector){
	$(selector).empty();
	$(selector).prepend('<div class="alert alert-success alert-dismissable">'+
	    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
	    message+'</div>');
    },
    
    sendpm:function(ev){
      var that = this;	
      if( $('#msgsub').val()!= '' &&  $('#newmessage').val() != ''){
	  $('#messagedialog').modal('hide');
	  window.getcsrf(function(csrf){
	      var dfrd = $.ajax({
		  url:window.ahr.app_urls.sendmessage+$('#usernameh').text(),
		  type: 'POST',
		  dataType: 'json',
		  data: {
		      csrfmiddlewaretoken :csrf.csrfmiddlewaretoken,
		      subject: $('#msgsub').val(),
		      message: $('#newmessage').val()
		  }
	      });
	      dfrd.done(function(){	       
		 $('#market').prepend('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>Your message was sent successfuly.</div>');
	      });
	  });    
      }else{
	  this.alert('Please provide a subject and message.','#pmerror');
      }    
    },

    
    cancelpm:function(ev){
    },

    showpMessage: function(ev){
        var username = ev.currentTarget.getAttribute('username');            
        $('#usernameh').text(username);
        $('#messagedialog').modal('show');
    }, 
    
    showRateuser: function(ev){
        var username = ev.currentTarget.getAttribute('username');
        var image_src = ev.currentTarget.getAttribute('image_src');
        var score = ev.currentTarget.getAttribute('score');
        var ratecount = ev.currentTarget.getAttribute('ratecount');
        $('#rateusertitle').text(username);
        $('#username').text(username);
        $('#ratecount').text(ratecount);
        $('#numstars').html('<div class="stars'+parseInt(Math.ceil(score))+'"></div>');
        $('#profileimage').attr('src',image_src);
        $('#rateuserdialog').modal('show');
    },
    
    setrate: function(ev){
        var that = this;
        if($('input[name="stars"]:checked').val() == undefined){
            this.alert('You have to select a rateing.','#rateerror');
            return;
        }
        window.getcsrf(function(csrf){
            var dfrd = $.ajax({
                url:window.ahr.app_urls.setuserrate+$('#username').text(),
                type: 'POST',
                dataType: 'json',
                data: {
                    score:$('input[name="stars"]:checked').val(),
                    csrfmiddlewaretoken :csrf.csrfmiddlewaretoken,
                    }
            });
            dfrd.done(function(data){
                $('.btn.rateuser').attr('ratecount',data.ratecount);
                $('.btn.rateuser').attr('score',data.score);
                $('#rateuserdialog').modal('hide');
                that.resetrate();
            });
            dfrd.fail(function(data){
                this.alert('Rating failed.','#rateerror');
            });
        });
    },
    
    resetrate: function(){
        $('input[name="stars"]:checked').prop('checked',false);
    },
});