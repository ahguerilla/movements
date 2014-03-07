(function(){

    var UserRoute = Backbone.Router.extend({
        routes:{
            "": "page"
        },

        page: function(page){
            this.users.initInfiniteScroll();
            $(window).scrollTop('100');
        },

        initialize: function(users){
            this.users=users;
        }
    });

    var UsersView = window.ahr.market.MarketBaseView.extend({
        types:{"Offers":"offer","Request":"request"},

        showItem: function(ev){
            window.location = $('a.linktoprofile',$(ev.currentTarget)).attr('href');
        },

        initialize : function(filters){
            var that = this;
            this.item_type = 'user';
            this.getitemfromto = window.ahr.app_urls.getuserfromto;
            this.viewurl = window.ahr.app_urls.viewuserprofile;
            this.item_tmp = _.template($('#user-template').html());
            this.item_widget = window.ahr.marketuser_widget.initWidget('body',that);

            filters.types=[];
            this.init(filters);
            window.ahr.expandTextarea('#newmessage');
            $('#q').typeahead({
               limit: 5,
               remote: window.ahr.app_urls['getusernames']+'?username=%QUERY'
               }).on('typeahead:selected', function (e, d) {
                 window.location = window.ahr.app_urls.viewuserprofile+d.value;
            });

            this.delegateEvents(_.extend(this.events,{
                'click .item_container': 'showItem'
            }));
            $('#filter-offer-text').text('Exchangivists Offering');
            $('#filter-request-text').text('Exchangivists Requesting');
            return this;
        },
    });

    window.ahr= window.ahr || {};
    window.ahr.users = window.ahr.users || {};
    window.ahr.users.initUsers = function(filters){
        $('#q').attr('placeholder','Search by keyword or username for Exchangivists');
        window.ahr.usersview = new UsersView(filters);
        var user_route = new UserRoute(window.ahr.usersview);
        Backbone.history.start();
        document.title = "Exchangivists";
    };

})();