(function(){
    window.ahr = window.ahr || {};
    window.ahr.item_form_base = window.ahr.BaseView.extend({
        el: '#itemform',
        init:function(){
            this.url = window.ahr.app_urls.addmarketitem+'';
        },

        submit: function(e){
            e.preventDefault();
            var that = this;
            $('.error').empty();

            var dfrd = $.ajax({
                type: 'POST',
                url: this.url,
                dataType:'json',
                traditional: true,
                data: this.getFormData()
            });
            dfrd.done(function(){
                if(that.aftersubmit){that.aftersubmit();}
                return true;
            });

            dfrd.fail(function(data){
                for(var item in data.responseJSON.errors){
                    $('.'+data.responseJSON.errors[item][0]+'.error',$(that.el)).html(data.responseJSON.errors[item][1]);
                }
                that.alert('Correct the errors (you have to select items from drop down menu)','#'+that.el.id+' #itemformerror');
            });

            return false;
        },

        initialize : function(item){
            var that= this;
            this.item_obj = null;
            this.delegateEvents(_.extend(this.events,{'submit' : 'submit'}));
            this.init();
            if(item !== false){
                that.url = window.ahr.app_urls.editmarketitem+item[0].pk;
                that.item_obj = item[0].fields;
            }
            that.makeWidget();
        }

   });

})();

