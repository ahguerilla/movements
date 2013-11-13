(function(){

    var SingleOfferView = Backbone.View.extend({
        el: '#offer-single',
        events:{
            'submit' : 'submit',
        },

    getFormData: function(){

    },

    getComment: function(coment,func){

    },


    setPage: function(){
        fields = this.item.fields;
        $('#marketitem_title').text(fields.title);
        $('#marketitem_owner').text(fields.owner[0]);
        $('#marketitem_date').text(fields.pub_date);
        $('#marketitem_details').text(fields.details);

        _.each(this.comments,function(comment){

            $.noop();
        });
    },

    initialize : function(obj_id){
        var that = this;
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

    window.offer_single = window.offer_single|| {};
    window.offer_single.initSingleOffer = function(obj_id){
        var offer = new SingleOfferView(obj_id);
    };
})();