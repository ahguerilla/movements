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

/*        addCommentCommentList: function(comment_item, front){
            front = front == true ? front : false
        }
*/
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
                            $('#newcomment').val("");
                            var comment_html = that.comment_tmp({pk:comment.pk,
                                user: "TO COME",
                                owner: "TO COME",
                                userpic: "TO COME",
                                pub_date: moment(new Date()).format("D MMM YYYY"),
                                content: comment
                            });
                            $('#marketitem_comments').prepend(comment_html);
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
            var that=this,
            fields = this.item.fields;
            $('#marketitem_type').text(fields.item_type.toUpperCase());
            $('#marketitem_title').text(fields.title);
            // TODO: should get returned by api
            $('#marketitem_owner').html("<a href='/user/profile/" + fields.owner[0] + "'>" + fields.owner[0] + "</a>");
            $('#marketitem_date').text(moment(fields.pub_date).format("D MMM YYYY"));
            $('#marketitem_details').html(fields.details.replace(/\n/g, '<br />'));

            _.each(this.comments,function(comment){
               var comment_html = that.comment_tmp({pk:comment.pk,
                            userpic: comment.fields.avatar,
                            user: comment.fields.username,
                            owner: comment.fields.owner,
                            pub_date: moment(comment.fields.pub_date).format("D MMM YYYY"),
                            content: comment.fields.contents
                        });
                $('#marketitem_comments').append(comment_html);
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