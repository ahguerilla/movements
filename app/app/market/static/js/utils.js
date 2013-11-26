window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.MarketBaseView = Backbone.View.extend({ 
	el: '#market',
    events:{
        'click .item_container': 'showItem',
        'click .tagbutton': 'tagsfilter',
        'click #searchbtn': 'search',
        'click .filter-type': 'changeFilterType',
        'click .item-type': 'itemTypesfilter'            
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

	initFilters: function(that,items,templ){           
	    _.each(window[items],function(item,key){            
	        if (that.filters[items].indexOf(parseInt(key))>-1){
	             $('.row.btn-group-sm.'+items).append(templ({filtertag:item, active:'btn-success'}));
	        }else{
	            $('.row.btn-group-sm.'+items).append(templ({filtertag:item, active:' '}));
	        }
	    }); 
	},

	updateTagsfilter: function(that,ev){	
		a=$(ev.currentTarget.parentElement.parentElement).attr("item_title");
		ar = that.filters[a];
		inv = invert(window[a]);
		if (inv.hasOwnProperty(ev.currentTarget.textContent)){
		    ind = inv[ev.currentTarget.textContent];
		    filtind = ar.indexOf(parseInt(ind));
		    if(filtind<0){
		        that.filters[a].push(parseInt(ind));
		        $(ev.currentTarget).addClass('btn-success');
		    }else{
		        that.filters[a].splice(filtind,1);
		        $(ev.currentTarget).removeClass('btn-success');
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
	 	for(item in types){
	 		$('.typetags').append(tmp({typetag:item}));
	 	}
	}

});



window.ahr.clone = function(obj) {
    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        var copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        var copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = window.ahr.clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        var copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = window.ahr.clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}