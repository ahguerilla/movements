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
        cancelpm:function(ev){},

        showpMessage: function(ev){
            var username = ev.currentTarget.getAttribute('username');
            //alert(username);
            $('#usernameh').text(username);
            $('#messagedialog').modal('show');
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
                'click .cancelpm': 'cancelpm'
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