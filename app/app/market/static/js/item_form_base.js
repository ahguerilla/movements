(function(){
    window.ahr = window.ahr || {};
    window.ahr.item_form_base = window.ahr.BaseView.extend({
        el: '#itemform',  
        init:function(){
            this.url = window.ahr.app_urls.addmarketitem+'';
        },
        
        submit: function(e){
            $('.error').empty();
            var that = this;
            e.preventDefault();
            var dfrd = $.ajax({
                type: 'POST',
                url: this.url,
                dataType:'json',
                traditional: true,
                data: this.getFormData()
            });
            dfrd.done(function(){
                window.location = window.ahr.app_urls.market;
            });
    
            dfrd.fail(function(data){
                for(var item in data.responseJSON.errors){
                    $('.'+data.responseJSON.errors[item][0]+'.error').html(data.responseJSON.errors[item][1]);
                }
                that.alert('Correct the errors (you have to select items from drop down menu)','#itemformerror');
            });
            return false;
        },
        
        initialize : function(item){
            var that= this;
            this.item_obj = null;
            this.delegateEvents(_.extend(this.events,{'submit' : 'submit'}));
            this.init()            ;
            if(item !== false){                
                that.url = window.ahr.app_urls.editmarketitem+item[0].pk;                    
                that.item_obj = item[0].fields;                
            }
            that.makeWidget();                        
        }

   });
    
})();

