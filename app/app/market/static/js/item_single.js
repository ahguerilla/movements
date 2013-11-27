(function(){

    var SingleItemView = Backbone.View.extend({
        el: '#item-single',
        events:{
            'click .comment-btn': 'comment'
        },

        getCommentData: function(){
            var dfrd = $.Deferred();
            window.getcsrf(function(csrf){
                dfrd.resolve(csrf);
            });
            return dfrd;
        },

        addCommentToCommentList: function(comment_item, front){
            front = front === true ? front : false;

            var comment_html = this.comment_tmp({pk:comment_item.pk,
                            userpic: comment_item.fields.avatar,
                            user: comment_item.fields.username,
                            owner: comment_item.fields.owner,
                            pub_date: moment(comment_item.fields.pub_date).format("D MMM YYYY"),
                            content: comment_item.fields.contents
                        });
            
            if(front){
                $('#marketitem_comments').prepend(comment_html);
            } else {
                $('#marketitem_comments').append(comment_html);
            }
        },

        comment: function(){
            var comment = $('#newcomment').val();
            var that = this;
            if(comment){
                var dfrd = this.getCommentData();
                dfrd.done(function(csrf){
                    var id = $('#item-single').attr('item-id');
                    $.ajax({
                        type: 'POST',
                        url: window.ahr.app_urls.addcomment+id,
                        dataType:'json',
                        data: {
                            "csrfmiddlewaretoken":csrf.csrfmiddlewaretoken,
                            "contents": comment
                        },
                        success: function(item){
                            console.log(item);
                            $('#newcomment').val("");
                            that.addCommentToCommentList(item.obj, true);
                        }
                    });
                });
            }
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
            
            fields = this.item.fields;
            $('#marketitem_type').text(fields.item_type.toUpperCase());
            $('#marketitem_title').text(fields.title);
            // TODO: should get returned by api
            $('#marketitem_owner').html("<a href='/user/profile/" + fields.owner[0] + "'>" + fields.owner[0] + "</a>");
            $('#marketitem_date').text(moment(fields.pub_date).format("D MMM YYYY"));
            $('#marketitem_details').html(fields.details.replace(/\n/g, '<br />'));

            var self = this;
            _.each(this.comments, function(comment){
                self.addCommentToCommentList(comment);
            });
        },
        

        initialize : function(obj_id){
            var that = this;
            this.comment_form_tmp = _.template($('#comment_add_template').html());
            $('#marketitem_comment_form').html(this.comment_form_tmp());

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
     
    });

    window.item_single = window.item_single|| {};
    window.item_single.initSingleItem = function(obj_id,obj_type){
        var item = new SingleItemView(obj_id,obj_type);
    };

})();