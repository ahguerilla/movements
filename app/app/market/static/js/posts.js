(function(){
    var PostsView = Backbone.View.extend({
        el: '#market',
        events:{
            'click .item_container': 'editItem'
        },

        editItem: function(ev){
            var id = ev.currentTarget.getAttribute('item_id');
            window.location = window.app_urls.edititem+id;
        },

        getItems: function(){
            return $.ajax({
                url:window.app_urls.getuseritems,
                dataType: 'json'
            });
        },

        initialize : function(obj_id){
            var that = this;
            this.item_tmp = _.template($('#item_template').html());

            var dfrd = this.getItems();
            dfrd.done(function(data){
                $.each(data, function(item){
                    data[item].fields.pk = data[item]. pk;
                    var item_html = that.item_tmp(data[item].fields);
                    $('#marketitems').append(item_html);
                });
            });
        },
});

    window.posts = window.posts || {};
    window.posts.initPosts = function(){
        var posts = new PostsView();
    };
})();