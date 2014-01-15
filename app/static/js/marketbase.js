window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = window.ahr.BaseView.extend({
    el: '#market',

    create_request: function(){
        this.requestdialog.showModal(true);
    },
    create_offer: function(){
        this.offerdialog.showModal(true);
    },

    setFilterNone:function(){
        $('.item-type').addClass('btn-success');
        this.filters = window.ahr.clone(this.default_filters);
        var skillarr=[];
        _.each(window.ahr.skills, function(item){
            skillarr.push(parseInt(item.pk, 10));
        });
        this.filters.skills =  skillarr;

        var countriesarr=[];
        _.each(window.ahr.countries, function(item){
            countriesarr.push(parseInt(item.pk, 10));
        });
        this.filters.countries =  countriesarr;

        var isssuesarr=[];
        _.each(window.ahr.issues, function(item){
            isssuesarr.push(parseInt(item.pk, 10));
        });
        this.filters.issues =  isssuesarr;
    },

    setFilterKeys:function(){
        var that = this;
        for(var key in this.filters){
            $('.row.'+key).empty();
            this.initFilters(that, key, that.tagtemp);
        }
    },

    changeFilterType: function(ev){
        var that = this;
        $('.filter-type').removeClass('btn-success');

        $(ev.currentTarget).addClass('btn-success');
        if(ev.currentTarget.textContent=="Default"){
            this.filters = window.ahr.clone(this.default_filters);
            $('.item-type').addClass('btn-success');
        }else if(ev.currentTarget.textContent=="All"){
            this.setFilterNone();
        }
        this.setFilterKeys();
        this.resetMarket();
    },

    showItem: function(ev){
        var id = ev.currentTarget.getAttribute('item_id');
        window.location = this.viewurl+id;
    },

    getItems: function(from,to,filters,aurl){
        filters.search=$('#q').val();
        return $.ajax({
            url: aurl.replace('0',from)+to,
            dataType: 'json',
            contentType:"application/json; charset=utf-8",
            data: filters,
            traditional: true
        });
    },

    getItemsCount: function(filters,aurl){
        return $.ajax({
            url: aurl,
            dataType: 'json',
            contentType:"application/json; charset=utf-8",
            data: filters,
            traditional: true
        });
    },

    setItems: function(page){
        var that = this;
        var dfrd = that.getItems(0+(10*page),
                    10+(10*page),
                    this.filters,
                    this.getitemfromto);

        dfrd.done(function(data){
            _.each(data, function(item){
                item.fields.pk = item.pk;
                var item_html = that.item_tmp(item.fields);
                $('#marketitems').append(item_html);
            });
        });

    },

    resetMarket: function(){
        $('#marketitems').empty();
        window.location.hash="";
        this.setItems(0);
        this.setpagecoutner(this.filters, this.itemcount_url);
    },

    setpagecoutner: function(filters, aurl){
        $(".marketitems.pagination").empty();
        var cdfrd = this.getItemsCount(filters,aurl);
        cdfrd.done(function(data){
            var pages = Math.ceil(data.count/10);
            for(i=1;i<=pages;i++){
                $(".marketitems.pagination").append("<li><a class='itempage' page='"+i+"' href='#p"+i+"'>"+i+"</a></li>");
            }
        });
    },

    initTemplates: function(){
        this.typetag_tmp = _.template($('#type-tag').html());
        this.tagtemp = _.template($('#filter-tag').html());
        for(var key in this.filters){
            if(["skills","countries","issues"].indexOf(key)>-1){
                this.initFilters(this, key, this.tagtemp);
            }
        }
        this.initTypeTags(this.types, this.typetag_tmp);
    },

    initFilters: function(that, items, templ){
        _.each(window.ahr[items], function(item){
            var activeFlag = ' ';
            if(_.contains(that.filters[items], item.pk)){
                 activeFlag = 'btn-success';
            }
            $('.row.btn-group-sm.'+items).append(templ({filtertag:item.value, active:activeFlag}));
        });
    },

    updateTagsfilter: function(that, ev){
        a=$(ev.currentTarget.parentElement.parentElement).attr("item_title");
        ar = that.filters[a];
        data = window.ahr[a];
        var tagData = _.find(data, function(test){
            return (test.value == ev.currentTarget.textContent);
        });
        if(tagData) {
            if(_.contains(ar, tagData.pk)){
                that.filters[a] = _.filter(ar, function(item){
                   return item != tagData.pk;
                });
                $(ev.currentTarget).removeClass('btn-success');
            } else {
                that.filters[a].push(tagData.pk);
                $(ev.currentTarget).addClass('btn-success');
            }
        }
    },

    updateTypefilter: function(that,ev){
        var ind = that.filters.types.indexOf(that.types[ev.currentTarget.textContent]);
        if(ind<0){
            that.filters.types.push(that.types[ev.currentTarget.textContent]);
            $(ev.currentTarget).addClass('btn-success');
        }else{
            that.filters.types.splice(ind,1);
            $(ev.currentTarget).removeClass('btn-success');
        }
    },

    initTypeTags: function(types,tmp){
        for(var item in types){
            $('.typetags').append(tmp({typetag:item}));
        }
    },

    setFilterType: function(ftype){
        $('.filter-type').removeClass('btn-success');
        $('.filter-type.'+ftype).addClass('btn-success');
    },

    search: function(){
        this.filters.search = $('#q').val();
        this.setFilterNone();
        this.setFilterKeys();
        this.resetMarket();
    },

    filterKeySearch: function(ev){
        ev.preventDefault();
        this.search();
        return false;
    },

    itemTypesfilter: function(ev){
        this.updateTypefilter(this,ev);
        this.resetMarket();
    },

    tagsfilter: function(ev){
        this.updateTagsfilter(this,ev);
        this.setFilterType("custom");
        this.resetMarket();
    },
    show_dropdown:function(ev){
        var item_id = ev.currentTarget.getAttribute('item_id');
        $('#dropdownMenu'+item_id).trigger('click');
        return(false);
    },

    init: function(filters){
        this.default_filters = window.ahr.clone(filters);

        this.requestdialog = window.ahr.request_form_dialog.initItem(false);
        this.offerdialog = window.ahr.offer_form_dialog.initItem(false);

        this.filters = filters;
        this.initTemplates(filters);
        this.filters.search=$('#q').val();
        this.setpagecoutner(this.filters, this.itemcount_url);
        this.delegateEvents(_.extend(this.events,{
            'click .item_container': 'showItem',
            'click .tagbutton': 'tagsfilter',
            'click #searchbtn': 'search',
            'click .filter-type': 'changeFilterType',
            'click .item-type': 'itemTypesfilter',
            'click #create_offer': 'create_offer',
            'click #create_request': 'create_request',
            'click .itemactions' : 'show_dropdown',
            'submit': 'filterKeySearch'
        }));
    }

});


