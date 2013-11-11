var typeAheadTag,
		widget =
		['<div class="row">',
			'<span class="col-xs-12"><%= title %></span>',
		'</div>',
		'<div class="row">',
			'<span class="col-xs-12 <%= item%>_error"></span>',
		'</div>',
		'<div class="row">',
			'<div class="col-xs-2">',
			  	'<div class="input-group">',
					'<input id="<%= item %>" class="form-control" type="text"/>',
					'<span class="input-group-btn">',
						'<button class="btn <%= item %>" type="button">Add</button>',
	      			'</span>',
		  		'</div>',
			'</div>',
		'</div>',

		'<div class="row">',
			'<div class="well col-xs-3">',
				'<div class="row" id="<%= item %>Tags"></div>',
			'</div>',
		'</div>'].join("");


typeAheadTag = _.template(widget);

var dict={};

function generateTypeAhead(title,  item){
	return typeAheadTag({'title':title,'item':item});
}


function makeTypeAhead(jsonfield, aurl){
	var typeaheadval = [],values=[];
	$.getJSON(aurl,function(data){
		for (var i = 0; i < data.length; i++){
			typeaheadval.push({
				tokens: [data[i].fields[jsonfield],],
				value: data[i].fields[jsonfield]
			});
			values.push(data[i].fields[jsonfield]);
			dict[data[i].fields[jsonfield]]=data[i].pk;
		}
		$('#'+jsonfield).typeahead({
			limit: 5,
			local: typeaheadval
			}).on('typeahead:selected', function (e, d) {
				$('#'+jsonfield).tagsManager("pushTag", d.value);
		});
	});
	return values;
}


function makeTagWidget(jsonfield, aurl){
	$('#'+jsonfield).tagsManager({
		tagsContainer: '#'+jsonfield+'Tags',
		deleteTagsOnBackspace: false,
		blinkBGColor_1: '#FFFF9C',
		blinkBGColor_2: '#CDE69C',
		hiddenTagListName: 'hidden-'+jsonfield,
		validator:function(tag){
			if (values.indexOf(tag)!=-1){
				return true;
			}else{
				return false;
			}
		},
	});
	var values = makeTypeAhead(jsonfield, aurl);
}


function getTagIds(name){
	var val_ids=[],
		val_names = $('input[name="hidden-'+name+'"]').val().split(',');
	_.each(val_names,function(val){
		val_ids.push(dict[val]);
	})
	return val_ids;
}


