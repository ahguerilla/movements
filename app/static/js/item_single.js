(function(){

    var SingleItemView = Backbone.View.extend({
        el: '#offer-single',
        events:{
            'submit' : 'submit',
        },

    getFormData: function(){

    },

    getComment: function(coment,func){

    },


    setPage: function(){
        var that=this,
        fields = this.item.fields;
        $('#marketitem_title').text(fields.title);
        $('#marketitem_owner').text(fields.owner[0]);
        $('#marketitem_date').text(fields.pub_date);
        $('#marketitem_details').text(fields.details);

        _.each(this.comments,function(comment){

            var comment = that.comment_tmp({pk:0,
                userpic:'test pic',
                user:'test user',
                pub_date:'test date',
                content:'test contents'});
            $('#marketitem_comments').append(comment);
        });
    },

    initialize : function(obj_id){
        var that = this;
        this.comment_tmp = _.template($('#comment_template').html());
        $.getJSON('/api/json/get/market/'+obj_id.id,function(data){
            that.item = data[0];
            $.getJSON('/api/json/get/comments/'+obj_id.id+'/last/100',function(data){
                that.comments = data;
                that.setPage();
            });
        });

    },

    submit: function(e){

    }
});

    window.item_single = window.item_single|| {};
    window.item_single.initSingleItem = function(obj_id){
        var offer = new SingleItemView(obj_id);
    };
})();