(function(){

    var CommentView = Backbone.View.extend({
        el: '#commentform',
        events:{
            'submit' : 'submit',
        },

    getFormData: function(){
        return {
            "contents": $('#id_contents').val(),
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
        }
    },

    getComment: function(coment,func){
        this.comment=$.getJSON(window.ahr.app_urls.getcomment+coment, func);
    },


    setForm: function(data){
        $('#id_contents').val(data[0].fields.contents);
    },

    initialize : function(coment,obj_id){
        if(coment === false){
            this.url = '/api/json/add/comment/'+obj_id;
        }else{
            var that=this;
            this.getComment(coment.id,function(comment_obj){
                that.url = window.ahr.app_urls.editcomment+comment_obj[0].pk;
                that.setForm(comment_obj);
            });
        }
    },

    submit: function(e){
        e.preventDefault();
        $.ajaxSetup({traditional: true});
        $.ajax({
            type: 'POST',
            url: this.url,
            dataType:'json',
            data: this.getFormData()
        });
        window.location = '/';
        return false;
    }
});

    window.comment = window.comment|| {};
    window.comment.initComment = function(coment,obj_id){
        var comment = new CommentView(coment, obj_id);
    };
})();