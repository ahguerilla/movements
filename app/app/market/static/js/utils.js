window.ahr = window.ahr || {};
window.ahr.market = window.ahr.market || {};

window.ahr.market.getItems = function(from,to,filters,aurl){
    filters.search=$('#q').val();
    return $.ajax({
        url: aurl.replace('0',from)+to,
        dataType: 'json',
        contentType:"application/json; charset=utf-8",
        data: filters,
        traditional: true
    });
}
        

window.ahr.market.getItemsCount = function(filters,aurl){           
    return $.ajax({               
        url: aurl,
        dataType: 'json',
        contentType:"application/json; charset=utf-8",
        data: filters,
        traditional: true
    });
}


window.ahr.market.setpagecoutner = function(filters, aurl){
    $(".marketitems.pagination").empty();
    var cdfrd = window.ahr.market.getItemsCount(filters,aurl);
    cdfrd.done(function(data){
        var pages = Math.ceil(data.count/10);
        for(i=1;i<=pages;i++){
            $(".marketitems.pagination").append("<li><a class='itempage' page='"+i+"' href='#p"+i+"'>"+i+"</a></li>");
        }
    });
}


window.ahr.market.initFilters = function(that,items,templ){           
    _.each(window[items],function(item,key){            
        if (that.filters[items].indexOf(parseInt(key))>-1){
             $('.row.btn-group-sm.'+items).append(templ({filtertag:item, active:'btn-success'}));
        }else{
            $('.row.btn-group-sm.'+items).append(templ({filtertag:item, active:' '}));
        }
    }); 
}



window.ahr.market.updateTagsfilter = function(that,ev){	
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
}

window.ahr.market.updateTypefilter = function(that,ev){
	var ind = that.filters.types.indexOf(that.types[ev.currentTarget.textContent]);
    if(ind<0){
        that.filters.types.push(that.types[ev.currentTarget.textContent]);
        $(ev.currentTarget).addClass('btn-success');
    }else{
        that.filters.types.splice(ind,1);
        $(ev.currentTarget).removeClass('btn-success');
    }
}