function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}

(function(){

    var ItemView = window.ahr.BaseView.extend({
        el: '#itemform',
        item_type: '',
        item:'',
        form_title:{
            'offer': 'OFFER A SERVICE',
            'resource': 'SHARE A RESOURCE',
            'request': 'REQUEST A SERVICE'
        },
        
        setWidgetArr:function(){    
            var that = this;
            this.widget_arrs = {
                'offer':[
                    {type: 'typeahead', title:'I can help to advance freedom of:', jsonfield:'issues', customGen: that.genTagWidget, customGet: that.getTagIds },
                    {type: 'typeahead', title:'Please select the countries where you can help',  jsonfield:'countries', customGen: that.genTagWidget, customGet: that.getTagIds},
                    {type: 'typeahead', title:'Skills',  jsonfield:'skills', customGen: that.genTagWidget, customGet:that.getTagIds},
                    {type: 'expdate', title:'Expires in days', jsonfield:'exp_date', customGet:that.getExpDate, customSet: that.setExpDate, placeholder:'' },
                    {type: 'input', title:'Title of post', jsonfield:'title', placeholder:''},
                    {type: 'textarea', title:'', jsonfield:'details', placeholder:'Please give details of what you can help with?'}
                ],
                'request':[
                    {type: 'typeahead', title:'I need help to advance freedom of:', jsonfield:'issues', customGen: that.genTagWidget, customGet: that.getTagIds},
                    {type: 'typeahead', title:'Please select the countries where you need help',  jsonfield:'countries', customGen: that.genTagWidget, customGet:that.getTagIds},
                    {type: 'datetimepicker', title:'Expiry date', jsonfield:'exp_date', placeholder:'', customSet:that.setDateTimePicker, afterGen:that.afterDateTimePicker },
                    {type: 'input', title:'Title of post', jsonfield:'title', placeholder:''},
                    {type: 'textarea', title:'', jsonfield:'details', placeholder:'Please give details of what you can help with?'}
                ],
                'resource':[
                    {type: 'typeahead', title:'Issues', jsonfield:'issues', customGen: that.genTagWidget, customGet:that.getTagIds },
                    {type: 'typeahead', title:'Country',  jsonfield:'countries', customGen: that.genTagWidget, customGet:that.getTagIds},
                    {type: 'typeahead', title:'Skills',  jsonfield:'skills', customGen: that.genTagWidget, customGet:that.getTagIds},
                    {type: 'datetimepicker', title:'Expiry date', jsonfield:'exp_date', placeholder:'', customSet:that.setDateTimePicker, afterGen:that.afterDateTimePicker },
                    {type: 'input', title:'Title of post', jsonfield:'title', placeholder:''},
                    {type: 'input', title:'URL link', jsonfield:'url', placeholder:''},
                    {type: 'textarea', title:'', jsonfield:'details', placeholder:'Add a description'}
                ]
            };
        },        
    
        getFormData: function(){
            var that = this;
            var retdict={};
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
            }else{
                var tmpl = _.template($('#'+item.type+'_template').html());
                var widget = tmpl({'title':item.title,
                    'jsonfield': item.jsonfield,
                    'placeholder': item.placeholder
                });
                $('#'+item.jsonfield+'_place').html(widget);
                if(preval){
                    if(item.customSet){
                        var func = _.bind(item.customSet,that);
                        func(item,preval);
                    }else{
                        $('#'+item.jsonfield).val(preval);
                    }
                }
            }
            if(item.afterGen){
                item.afterGen(item);
            }
        },
    
        initialize : function(item, obj_type){
            var that= this;
            this.setWidgetArr();
            this.item_type = obj_type;
            this.delegateEvents(_.extend(this.events,{'submit' : 'submit'}));
            if(item === false){
                $('#form-title').html(that.form_title[that.item_type]);
                this.url = window.ahr.app_urls.addmarketitem+obj_type;
                _.each(this.widget_arrs[obj_type],function(item){
                    that.makeWidget(item);
                });
            }else{
                this.getItem(item,function(item_obj){
                    that.url = window.ahr.app_urls.editmarketitem+item_obj[0].pk;
                    that.item_type = item_obj[0].fields.item_type;
                    that.item_obj = item_obj[0].fields;
                    that.setForm(item_obj, that.item_type);
                    $('#form-title').html(that.form_title[that.item_type]);
                });
            }
    
        },
    
        submit: function(e){
            $('.error').empty()
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
                for(item in data.responseJSON.errors){
                    $('.'+data.responseJSON.errors[item][0]+'.error').html(data.responseJSON.errors[item][1]);
                }
                that.alert('Correct the errors (you have to select items from drop down menu)','#itemformerror');
            });
            return false;
        }
    });

    window.item_form = window.item_form|| {};
    window.item_form.initItem= function(item,obj_type){
        var item_form = new ItemView(item,obj_type);
    };
})();

