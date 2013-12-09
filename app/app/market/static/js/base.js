(function(){

    setInterval(function(){
        var text;
        $.getJSON(window.ahr.app_urls.getmessagecount,function(data){
            $('.message-counter').each(function(tmp,item){
                if(data>0){
                   $('#msgcntr',$(item)).text('('+data+')');
                }
            });
        });
    },30000);

    window.ahr= window.ahr || {};
    window.ahr.BaseView = Backbone.View.extend({
        tagdict: {},
        events:{
            'click .sendprivatemessageuser': 'showpMessage',
            'click .sendpm': 'sendpm',
            'click .cancelpm': 'cancelpm',
            'click .btn.rate': 'showrate',
            'click .sendrate': 'setrate',
            'click .cancelrate': 'resetrate',
            'click #expdate-neverexpire': 'neverexp',
        },

        invert: function (obj) {
            var new_obj = {};
            for (var prop in obj) {
                if(obj.hasOwnProperty(prop)) {
                    new_obj[obj[prop]] = prop;
                }
            }
            return new_obj;
        },

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
            }else{
                val = $('#'+data).val();
            }

            if(val===""){return "";}
            var date = moment().add('days',parseInt(val)+1).format("D/M/YYYY HH:m");
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
        },

        alert: function(message,selector){
            $(selector).empty();
            $(selector).prepend('<div class="alert alert-warning alert-dismissable">'+
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
            message+'</div>');
        },

        info: function (message,selector){
            $(selector).empty();
            $(selector).prepend('<div class="alert alert-success alert-dismissable">'+
                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                message+'</div>');
        },

        sendpm: function(ev){
            var that = this;
                if( $('#msgsub').val()!== '' &&  $('#newmessage').val() !== ''){
                $('#messagedialog').modal('hide');
                window.ahr.getcsrf(function(csrf){
                    var dfrd = $.ajax({
                        url:window.ahr.app_urls.sendmessage+$('#usernameh').text(),
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            csrfmiddlewaretoken :csrf.csrfmiddlewaretoken,
                            subject: $('#msgsub').val(),
                            message: $('#newmessage').val()
                        }
                    });
                    dfrd.done(function(){
                        $('#market').prepend('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>Your message was sent successfuly.</div>');
                    });
                });
            }else{
                this.alert('Please provide a subject and message.','#pmerror');
            }
        },


        cancelpm: function(ev){
        },

        showpMessage: function(ev){
            var username = ev.currentTarget.getAttribute('username');
            $('#usernameh').text(username);
            $('#msgsub').val('');
            $('#newmessage').val('');
            $('#messagedialog').modal('show');
        },

        showrate: function(ev){
            var username = ev.currentTarget.getAttribute('username');
            var image_src = ev.currentTarget.getAttribute('image_src');
            var score = ev.currentTarget.getAttribute('score');
            var ratecount = ev.currentTarget.getAttribute('ratecount');
            $('#ratetitle').text(username);
            $('#username').text(username);
            $('#ratecount').text(ratecount);
            $('#numstars').html('<div class="stars'+parseInt(Math.round(score))+'"></div>');
            $('#profileimage').attr('src',image_src);
            $('#ratedialog').modal('show');
        },

        setrate: function(ev){
            var that = this;
            if($('input[name="stars"]:checked').val() == undefined){
                this.alert('You have to select a rateing.','#rateerror');
                return;
            }
            window.ahr.getcsrf(function(csrf){
                if ($('.btn.rate').attr('rateing')=='user'){
                    this.rateurl = window.ahr.app_urls.setuserrate+$('#username').text();
                }else{
                }
                var dfrd = $.ajax({
                    url: this.rateurl,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        score:$('input[name="stars"]:checked').val(),
                        csrfmiddlewaretoken :csrf.csrfmiddlewaretoken,
                        }
                });
                dfrd.done(function(data){
                    $('.btn.rate').attr('ratecount',data.ratecount);
                    $('.btn.rate').attr('score',data.score);
                    $('#ratedialog').modal('hide');
                    that.resetrate();
                });
                dfrd.fail(function(data){
                    that.alert('Rating failed.','#rateerror');
                });
            });
        },

        resetrate: function(){
            $('input[name="stars"]:checked').prop('checked',false);
        },
    });
})();


window.ahr.expandTextarea= function(id) {
    var $element = $(id).get(0);

    $element.addEventListener('keyup', function() {
        this.style.overflow = 'hidden';
        this.style.height = 0;
        var sh = this.scrollHeight;
        if(sh<100){
            sh = 100;
        }
        this.style.height =  sh+10 + 'px';
    }, false);
};

