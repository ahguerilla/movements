(function(){
    $('.nanamorde').hide();
    var UserRoute = Backbone.Router.extend({
        routes:{
            "": "page"
        },

        page: function(page){
            this.users.showMarket();
            this.users.initInfiniteScroll();
            this.users.scrollBack();
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
            this.init(filters);
            this.filter_widget.filters.types = ['offer', 'request'];
            this.filter_widget.types = this.types;

            window.ahr.expandTextarea('#newmessage');
            $('#q').typeahead({
               limit: 5,
               remote: window.ahr.app_urls['getusernames']+'?username=%QUERY'
               }).on('typeahead:selected', function (e, d) {
                 window.location = window.ahr.app_urls.viewuserprofile+d.value;
            });

            $('#filter-offer-text').text(window.ahr.string_constants.offering);
            $('#filter-request-text').text(window.ahr.string_constants.requesting);
            $('#info-panel-container').remove();
            $('#singleItem').show();

            this.events = _.extend(this.events,{
                'click .item_container': 'showItem'
            });
            this.filter_widget.HideShowHidden();
            return this;
        },
    });
    window.ahr= window.ahr || {};
    window.ahr.users = window.ahr.users || {};
    window.ahr.users.initUsers = function(filters){
        $('#q').attr('placeholder', window.ahr.string_constants.user_search_by_params);
        window.ahr.usersview = new UsersView(filters);
        var user_route = new UserRoute(window.ahr.usersview);
        Backbone.history.start();
        document.title = window.ahr.string_constants.members;
    };

})();