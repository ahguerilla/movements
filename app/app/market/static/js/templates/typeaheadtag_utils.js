var typeAheadTag;

$(document).ready(function(){
	typeAheadTag = _.template($('#typeahead_template').html());
});

window.tagdict={};

var invert = function (obj) {
  var new_obj = {};
  for (var prop in obj) {
    if(obj.hasOwnProperty(prop)) {
      new_obj[obj[prop]] = prop;
    }
  }
  return new_obj;
};


function generateTypeAhead(title,  item){
	return typeAheadTag({'title':title,'item':item});
}


function makeTypeAhead(jsonfield, aurl,func){
	var typeaheadval = [],values=[];
	$.getJSON(aurl,function(data){
		for (var i = 0; i < data.length; i++){
			typeaheadval.push({
				tokens: [data[i].fields[jsonfield],],
				value: data[i].fields[jsonfield]
			});
			values.push(data[i].fields[jsonfield]);
			window.tagdict[data[i].fields[jsonfield]]=data[i].pk;
		}
		$('#'+jsonfield).typeahead({
			limit: 5,
			local: typeaheadval
			}).on('typeahead:selected', function (e, d) {
				$('#'+jsonfield).tagsManager("pushTag", d.value);
		});
	func(values);
	});
}


function makeTagWidget(jsonfield, aurl,prefilled){
	makeTypeAhead(jsonfield, aurl,function(data){
		var pref=[],values = data;
		if (prefilled){
			inv = invert(window.tagdict);
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
			},
		});
	});
}


function getTagIds(name){
	var val_ids=[],
		val_names = $('input[name="hidden-'+name+'"]').val().split(',');
	_.each(val_names,function(val){
		val_ids.push(window.tagdict[val]);
	});
	return val_ids;
}


function genTagWidget(item, preval){
	$('#'+item.jsonfield+'_place').html(generateTypeAhead(item.title, item.jsonfield));
	if (item.jsonfield == 'skills'){
		makeTagWidget(item.jsonfield,window.ahr.app_urls.getskills, preval);
	}else if (item.jsonfield == 'issues'){
		makeTagWidget(item.jsonfield,window.ahr.app_urls.getissues, preval);
	}else{
		makeTagWidget(item.jsonfield,window.ahr.app_urls.getcountries, preval);
	}
	
}