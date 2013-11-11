(function(){

	var OfferView = Backbone.View.extend({
		el: '#offerform',
		events:{
				'submit' : 'submit',
  		},
  		ar:[
			{title:'I can help to advance freedom of:', jsonfield:'issues'},
			{title:'Please select the countries where you can help',  jsonfield:'countries'},
			{title:'Skills',  jsonfield:'skills'}
		],

		getFormData: function(){
			return {"issues": getTagIds('issues'),
					"countries": getTagIds('countries'),
					"skills": getTagIds('skills'),
					"exp_date": $('#exp-date').val(),
					"title": $('#post-title').val(),
					"details": $('#details').val(),
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				}
		},

		initialize : function(offer){
			if(offer===""){
				$('#datetimepicker1').datetimepicker({format:'D/M/YYYY HH:mm'});
				_.each(this.ar,function(item){
					$('#'+item.jsonfield+'place').html(generateTypeAhead(item.title, item.jsonfield));
					makeTagWidget(item.jsonfield,'/api/'+item.jsonfield+'/json');
				});
			}else{
				$('#datetimepicker1').datetimepicker({format:'D/M/YYYY HH:mm'});
				$('#exp-date').val('12/11/2013 14:23');
			}
		},

		submit: function(e){
			e.preventDefault();
			$.ajaxSetup({traditional: true});
			$.ajax({
				type: 'POST',
				url: '/api/new/offer',
				dataType:'json',
				data: this.getFormData()
			});
			return false;
		}
	});

	window.offer = window.offer|| {};
	window.offer.initOffer = function(offer){
  		var offer = new OfferView(offer);
	};
})();