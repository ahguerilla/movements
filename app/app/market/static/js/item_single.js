(function(){

    var SingleItemView = window.ahr.BaseView.extend({
        el: '#item-single',

        cancel_message: function(){
            $('#marketitem_message_form').addClass('hide');
            $('#marketitem_comment_form').show();
        },

        send_message: function(){
            $('#marketitem_message_form').addClass('hide');
            $('#marketitem_comment_form').show();
            var that = this;
            window.ahr.getcsrf(function(csrf){
                var dfrd = $.ajax({
                    url:window.ahr.app_urls.sendmessage+that.item.fields.owner[0],
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        csrfmiddlewaretoken :csrf.csrfmiddlewaretoken,
                        subject: $('#msgsub').val(),
                        message: $('#newmessage').val()
                    }
                });
                dfrd.done(function(){
                   that.info('Your message was sent successfuly.','#infobar');
                   $('#marketitem_comment_form').show();
                });
                dfrd.fail(function(){
                    that.alert('Unable to send message now. Please try again.','#infobar');
                    $('#marketitem_message_form').removeClass('hide');
                    $('#marketitem_comment_form').hide();
                });
            });
        },

        reportPostClicked: function(){
            this.showModalDialog('#report_template', {}, '#reportdialog', function(){
                $('#reportdialog .send').click(function(){
                    window.ahr.getcsrf(function(csrf){
                        $.ajax({
                            type: "POST",
                            url: window.ahr.app_urls.reportpost + '1',
                            dataType: 'json',
                            data: {
                                "csrfmiddlewaretoken": csrf.csrfmiddlewaretoken,
                                "contents": $("#reportdialog #content").val()
                            },
                            success: function(data) {
                                console.log(data);
                            },
                            statusCode: {
                                400: function(data) { console.log(data); },
                            }
                        });
                    });
                });

                $('#reportdialog .cancel').click(function(){
                });
            });
        },

        private_message: function(){
            $('#msgsub').val('Re: '+$('#marketitem_title').text());
            $('#marketitem_comment_form').hide();
            $('#newmessage').css('height','110px');
            $('#newmessage').val('');
            $('#marketitem_message_form').removeClass('hide');
        },

        getCommentData: function(){
            var dfrd = $.Deferred();
            window.ahr.getcsrf(function(csrf){
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
                            owner_url: comment_item.fields.profile_url,
                            pub_date: moment(comment_item.fields.pub_date).format("D MMM YYYY"),
                            content: comment_item.fields.contents.replace(/\n/g, '<br />')
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
                            $('#newcomment').val("");
                            that.addCommentToCommentList(item.obj, true);
                        }
                    });
                });
            }
        },

        setPage: function(){

            fields = this.item.fields;
            $('#marketitem_type').text(fields.item_type.toUpperCase());
            $('#marketitem_title').text(fields.title);
            // TODO: should get returned by api
            $('#marketitem_owner').html("<a href='/user/profile/" + fields.owner[0] + "'>" + fields.owner[0] + "</a>");
            $('#marketitem_date').text(moment(fields.pub_date).format("D MMM YYYY"));
            $('#marketitem_details').html($('<div/>').text(fields.details).html().replace(/\n/g, '<br />'));
            var self = this;
            _.each(this.comments, function(comment){
                self.addCommentToCommentList(comment);
            });
        },


        initialize : function(obj_id){
            var that = this;
            window.ahr.expandTextarea('#newmessage');
            this.comment_form_tmp = _.template($('#comment_add_template').html());
            $('#marketitem_comment_form').html(this.comment_form_tmp());
            window.ahr.expandTextarea('#newcomment');
            this.comment_tmp = _.template($('#comment_view_template').html());
            
            this.delegateEvents(_.extend(this.events,{
                'click .comment-btn': 'comment',
                'click #private_message': 'private_message',
                'click #cancel_message': 'cancel_message',
                'click #send_message': 'send_message',
                'click #report_post': 'reportPostClicked'
            }));
            
            $.getJSON(
                window.ahr.app_urls.getmarketitem+obj_id.id,
                function(data){
                    that.item = data[0];
                    if(that.item.fields.item_type == "resource"){
                        $('#rate_resource').removeClass('hidden');
                        $('#rate_resource').attr('username',that.item.fields.owner[0]);
                        $('#rate_resource').attr('ratecount',that.item.fields.userratecount);
                        $('#rate_resource').attr('score',that.item.fields.usercore);
                        $('#rate_resource').attr('image_src',that.item.fields.avatar);
                    }else{
                        $.noop();
                    }
                    $('#rate_user').attr('username',that.item.fields.owner[0]);
                    $('#rate_user').attr('ratecount',that.item.fields.userratecount);
                    $('#rate_user').attr('score',that.item.fields.usercore);
                    $('#rate_user').attr('image_src',that.item.fields.avatar);
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