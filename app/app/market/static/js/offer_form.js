(function(){

    var OfferView = window.ahr.item_form_base.extend({        
        item_type: '',
        item:'',        
        
        setWidgetArr:function(){
            var that = this;
            this.widget_arrs = {
                'offer':[                                        
                    {type: 'expdate', title:'Expires in days', jsonfield:'exp_date', customGet:that.getExpDate, customSet: that.setExpDate, placeholder:'' },
                    {type: 'input', title:'Title of post', jsonfield:'title', placeholder:''},
                    {type: 'textarea', title:'', jsonfield:'details', placeholder:'Please give details of what you can help with?'}
                ]
            };
        },
    
        getFormData: function(){
            var that = this;
            var retdict={};  
            retdict['skills'] = this.skills_widget.getTagIds();
            retdict['countries'] = this.countries_widget.getTagIds();
            retdict['issues'] = this.issues_widget.getTagIds();
            _.each(this.widget_arrs[this.item_type],function(item){
                if(item.customGet){
                    var func = _.bind(item.customGet,that);
                    retdict[item.jsonfield] = func(item.jsonfield);
                }else{
    
                    retdict[item.jsonfield] = $('#'+item.jsonfield).val();
                }
            });
            retdict.csrfmiddlewaretoken=$('input[name="csrfmiddlewaretoken"]').val();
            return retdict;
        },
    
        getItem: function(item,func){
            this.item=$.getJSON(window.ahr.app_urls.getmarketitem + item.id, func);
        },
    
        setForm: function(data,obj_type){
            var that=this;
            tempfields = data[0].fields;
    
            _.each(this.widget_arrs[obj_type],function(item){
                that.makeWidget(item,tempfields[item.jsonfield]);
            });
        },
    
        makeWidget: function(item,preval){
            var that = this;
            if(item.customGen){
                var func = _.bind(item.customGen,this);
                func(item,preval);
            } else {
                var tmpl = _.template($('#'+item.type+'_template').html());
                var widget = tmpl({'title':item.title,
                    'jsonfield': item.jsonfield,
                    'placeholder': item.placeholder
                });
                $('#'+item.jsonfield+'_place').html(widget);
                if(preval){
                    if(item.customSet){
                        var func2 = _.bind(item.customSet,that);
                        func2(item,preval);
                    }else{
                        $('#'+item.jsonfield).val(preval);
                    }
                }
            }
            if(item.afterGen){
                item.afterGen(item);
            }
        },
    
        initialize : function(item){
            var that= this;
            this.setWidgetArr();
            this.item_type = 'offer';
            this.item_obj = null;
            this.delegateEvents(_.extend(this.events,{'submit' : 'submit'}));
            if(item === false){                
                this.url = window.ahr.app_urls.addmarketitem+'offer';
                this.issues_widget = window.ahr.typeahead_widget.initWidget(
                            '#issues_place',
                            {title:'I can help to advance freedom of:', jsonfield:'issues'});
                this.countries_widget = window.ahr.typeahead_widget.initWidget(
                            '#countries_place',
                            {title:'Please select the countries where you can help',  jsonfield:'countries'});
                this.skills_widget = window.ahr.typeahead_widget.initWidget(
                            '#skills_place',
                            {title:'Skills',  jsonfield:'skills'});
                _.each(this.widget_arrs['offer'],function(item){
                    that.makeWidget(item);
                });
            } else {
                this.getItem(item,function(item_obj){
                    that.url = window.ahr.app_urls.editmarketitem+item_obj[0].pk;
                    that.item_type = item_obj[0].fields.item_type;
                    that.item_obj = item_obj[0].fields;
                    that.setForm(item_obj, that.item_type);                    
                });
            }
    
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
        }
    });

    window.ahr.offer_form = window.ahr.offer_form|| {};
    window.ahr.offer_form.initItem= function(item){
        var offer_form = new OfferView(item);
    };
})();


