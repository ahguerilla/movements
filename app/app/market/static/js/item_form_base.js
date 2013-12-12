(function(){
    window.ahr = window.ahr || {};
    window.ahr.item_form_base = window.ahr.BaseView.extend({
        el: '#itemform',
        neverexp: function(ev){
            if($(ev.currentTarget).prop('checked') === false){
                $('#exp_date').attr('readonly',false);
                $('#exp_date').show();
            }else{
                $('#exp_date').attr('readonly',true);
                    $('#exp_date').hide();
            }
        },
        setExpDate: function(item,date){
            //tz = jstz.determine();
            //tzName = tz.name();
            //ad=moment.utc(date).tz(tzName).format();
            days = moment(date).diff(moment(),'days');
            $('#'+item.jsonfield).val(days);
            if (moment(this.item_obj.pub_date).diff(moment(date),'days') == -36501){
                $('#exp_date').attr('readonly',true);
                    $('#exp_date').hide();
                $('#expdate-neverexpire').prop('checked',true);
            }
        },
        
        getExpDate: function(data){
            var val;
            if($('#expdate-neverexpire').prop('checked') === true){
                val = 36500;
            } else {
                val = $('#'+data).val();
            }
        
            if(val===""){return "";}
            var date = moment().add('days', parseInt(val, 10) + 1).format("D/M/YYYY HH:m");
            return date;
        },
          

        generateTypeAhead: function(title,  item){
            if (this.typeAheadTag  === undefined){
                this.typeAheadTag = _.template($('#typeahead_template').html());
            }
            return this.typeAheadTag({'title':title,'item':item});
        },

        setDateTimePicker: function(item,preval){
            if(preval){
                $('#'+item.jsonfield).val(preval.slice(8,10)+'/'+
                    preval.slice(5,7)+'/'+
                    preval.slice(0,4)+' '+
                    preval.slice(11,13)+':'+
                    preval.slice(14,16)
                );
            }
        },

        makeTypeAhead: function(jsonfield, aurl,func){
            var that = this;
            var typeaheadval = [],values=[];
            $.getJSON(aurl,function(data){
                for (var i = 0; i < data.length; i++){
                    typeaheadval.push({
                        tokens: [data[i].fields[jsonfield],],
                        value: data[i].fields[jsonfield]
                    });
                    values.push(data[i].fields[jsonfield]);
                    that.tagdict[data[i].fields[jsonfield]]=data[i].pk;
                }
                $('#'+jsonfield).typeahead({
                    limit: 5,
                    local: typeaheadval
                    }).on('typeahead:selected', function (e, d) {
                        $('#'+jsonfield).tagsManager("pushTag", d.value);
                }).blur(function(){
                    $('#'+jsonfield).val('');
                });
                func(values);
            });
        },

        makeTagWidget: function (jsonfield, aurl, prefilled){
            var that = this;
            this.makeTypeAhead(jsonfield, aurl,function(data){
                var pref=[],values = data;
                if (prefilled){
                    inv = that.invert(that.tagdict);
                    _.each(prefilled,function(id){
                        pref.push(inv[id]);
                    });
                }

                $('#'+jsonfield).tagsManager({
                    tagsContainer: '#'+jsonfield+'Tags',
                    deleteTagsOnBackspace: false,
                    blinkBGColor_1: '#FFFF9C',
                    blinkBGColor_2: '#CDE69C',
                    hiddenTagListName: 'hidden-'+jsonfield,
                    prefilled: pref,
                    validator:function(tag){
                        if (values.indexOf(tag)!=-1){
                            return true;
                        }else{
                            return false;
                        }
                    }
                });
            });
        },

        getTagIds: function(name){
            var that = this;
            var val_ids=[],
                val_names = $('input[name="hidden-'+name+'"]').val().split(',');
            _.each(val_names,function(val){
                val_ids.push(that.tagdict[val]);
            });
            return val_ids;
        },

        genTagWidget: function (item, preval){
            var that = this;
            $('#'+item.jsonfield+'_place').html(that.generateTypeAhead(item.title, item.jsonfield));
            if (item.jsonfield == 'skills'){
                this.makeTagWidget(item.jsonfield,window.ahr.app_urls.getskills, preval);
            }else if (item.jsonfield == 'issues'){
                this.makeTagWidget(item.jsonfield,window.ahr.app_urls.getissues, preval);
            }else{
                this.makeTagWidget(item.jsonfield,window.ahr.app_urls.getcountries, preval);
            }

        },

        afterDateTimePicker: function(item){
            $('#'+item.type+'-'+item.jsonfield).datetimepicker({format:'D/M/YYYY HH:mm'});
        }

   });
    
})();

