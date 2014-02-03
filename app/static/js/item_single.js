(function(){

    var SingleItemView = window.ahr.BaseView.extend({
        el: '#item-single',

        recommend: function(){
            $('#recsub').val($('#currentusername').text()+' recommends: '+ this.item.fields.title);
            $('#recsub').attr('readonly',true);
            var href = '<a href="'+window.location+'">'+this.item.fields.title+'</a>';
            $('#recmessage').val($('#currentusername').text()+ ' recommends you have a look at this '+ this.item.fields.item_type+ ' by '+ this.item.fields.owner+' \r\n'+ href );
            $('#touser').val('');
            $('#recommenddialog').modal('show');
        },

        reportPostClicked: function(){
            var that = this;
            this.showModalDialog('#report_template', {}, '#reportdialog', function(){
                $('#reportdialog .send').click(function(){
                    window.ahr.getcsrf(function(csrf){
                        if(csrf==false){
                            that.alert('Unable to send report. please try again','#reporterror');
                            return;
                        }
                        $.ajax({
                            type: "POST",
                            url: window.ahr.app_urls.reportpost + $('#item-single').attr('item-id'),
                            dataType: 'json',
                            data: {
                                "csrfmiddlewaretoken": csrf.csrfmiddlewaretoken,
                                "contents": $("#reportdialog #content").val()
                            },
                            success: function(data) {
                                console.log(data);
                                that.info('Report sent succesfuly','#infobar');
                                $('#reportdialog').modal('hide');
                            },
                            statusCode: {
                                400: function(data) {
                                    console.log(data);
                                    that.alert('Unable to send report. please try again','#reporterror');
                                },
                            }
                        });
                    });
                });
                $('#reportdialog .cancel').click(function(){
                });
            });
        },

        private_message: function(ev){
            var username = ev.currentTarget.getAttribute('username');
            var msgsub = 'Re: '+$('#marketitem_title').text();
            this.message_widget.show(username,msgsub,'',true);

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
        deleteComment:function(ev){
            var that = this;
            if(confirm('Are you sure you want yo delete your comment?')){
                var comment_id =  ev.currentTarget.getAttribute('comment-id');
                var aurl = $('a',$(ev.currentTarget))[0];
                var dfrd = $.ajax({url:aurl.href});
                dfrd.success(function(data){
                    that.alert('Your comment was deleted.','#infobar');
                    $('.comment[comment-id="'+comment_id+'"]').remove();
                });
            }
            return false;
        },

        setPage: function(){
            fields = this.item.fields;
            $('#marketitem_type').text(fields.item_type.toUpperCase());
            $('#marketitem_title').text(fields.title);
            // TODO: should be returned by api
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

            this.rate_widget = window.ahr.rate_form_dialog.initWidget('#'+this.el.id);
            this.message_widget = window.ahr.messagedialog_widget.initWidget('#'+this.el.id,'#infobar');

            this.delegateEvents(_.extend(this.events,{
                'click .comment-btn': 'comment',
                'click #private_message': 'private_message',
                'click #recommend': 'recommend',
                'click #report_post': 'reportPostClicked',
                'click .comment-delete': 'deleteComment'
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
                    window.ahr.recommend_widget.initWidget(that.item.fields.owner[0]);
                    $('#recommend').attr('username',that.item.fields.owner[0]);
                    $('#private_message').attr('username',that.item.fields.owner[0]);
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