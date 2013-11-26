(function(){

    var SingleItemView = Backbone.View.extend({
        el: '#item-single',
        events:{
            'submit' : 'submit',
        },

    getFormData: function(){

    },

    getComment: function(coment,func){

    },

    getUserAvatar: function(id,callback){
        return $.ajax({
            url: window.ahr.app_urls.getavatar+id,
            dataType: "json",
        });
    },

    getUserDetail: function(id,callback){    
        return $.ajax({
            url: window.ahr.app_urls.getuserdetail+id,
            dataType: "json",
            });
    },


    setPage: function(){
        var that=this,
        fields = this.item.fields;
        $('#marketitem_title').text(fields.title);
        $('#marketitem_owner').text(fields.owner[0]);
        $('#marketitem_date').text(moment(fields.pub_date).format("D MMM YYYY"));
        $('#marketitem_details').html(fields.details);

        _.each(this.comments,function(comment){
            var username, avatar, username_dfrd, avatar_dfrd;

            avatar_dfrd = that.getUserAvatar(comment.fields.owner);
            username_dfrd = that.getUserDetail(comment.fields.owner);

            avatar_dfrd.done(function(data){
               avatar = '/media/'+data[0].fields.avatar;
               username_dfrd.done(function(data){
                    username = data[0].fields.username;
                    var comment_html = that.comment_tmp({pk:comment.pk,
                        userpic: avatar,
                        user: username,
                        pub_date: moment(comment.fields.pub_date).format("D MMM YYYY"),
                        content: comment.fields.contents});

                    $('#marketitem_comments').append(comment_html);
                });   
            });            
        });
    },
    

    initialize : function(obj_id){
        var that = this;
        this.comment_tmp = _.template($('#comment_view_template').html());
        $.getJSON(
            window.ahr.app_urls.getmarketitem+obj_id.id,
            function(data){
                that.item = data[0];
                $.getJSON(window.ahr.app_urls.getcommentslast.replace('0',obj_id.id)+'100',function(data){
                    that.comments = data;
                    that.setPage();
                });
        });

    },

    submit: function(e){

    }
});

    window.item_single = window.item_single|| {};
    window.item_single.initSingleItem = function(obj_id,obj_type){
        var item = new SingleItemView(obj_id,obj_type);
    };
})();