(function(){

    var UserRoute = Backbone.Router.extend({
        routes:{
            "": "page",
            "p:page": "page"
        },

        page: function(page){
            if(page){
                $('#marketitems').empty();
                this.users.setItems(parseInt(page)-1);
            }else{
                this.users.setItems(0);
            }
        },

        initialize: function(users){
            this.users=users;
        }
    });

    var UsersView = window.ahr.market.MarketBaseView.extend({
        types:{"Activist" : "activist", "Ready to help" : "readytohelp" },

        sendpm:function(ev){
            var that = this;
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
                   $('#messagedialog').modal('hide');
                   $('#market').prepend('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>Your message was sent successfuly.</div>');
                });
            });
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

        initialize : function(filters){
            this.itemcount_url = window.ahr.app_urls.getusercount;
            this.getitemfromto = window.ahr.app_urls.getuserfromto;
            this.viewurl = window.ahr.app_urls.viewuserprofile;
            this.item_tmp = _.template($('#user-template').html());
            filters.types=["activist", "readytohelp"];
            this.init(filters);
            window.ahr.expandTextarea('#newmessage');
            this.delegateEvents(_.extend(this.events,{
                'click .sendprivatemessageuser': 'showpMessage',
                'click .sendpm': 'sendpm',
                'click .cancelpm': 'cancelpm',
                'click .rateuser': 'showRateuser',
                'click .sendurate': 'setrate',
                'click .cancelrate': 'resetrate'
            }));
            return this;
        },
    });

    window.ahr= window.ahr || {};
    window.ahr.users = window.ahr.users || {};
    window.ahr.users.initUsers = function(filters){
        var users = new UsersView(filters);
        var user_route = new UserRoute(users);
        Backbone.history.start();
    };

})();