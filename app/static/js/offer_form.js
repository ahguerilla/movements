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

		getOffer: function(offer,func){
			this.offer=$.getJSON('/api/json/get/market/'+offer.id, func);
		},

		setExpDate: function(datestr){
			$('#exp-date').val(datestr.slice(8,10)+'/'+
				datestr.slice(5,7)+'/'+
				datestr.slice(0,4)+' '+
				datestr.slice(11,13)+':'+
				datestr.slice(14,16));
		},

		setForm: function(data){
			var fields;
			window.tempfields = fields = this.fields = data[0].fields;

			$('#datetimepicker1').datetimepicker({format:'D/M/YYYY HH:mm'});
			this.setExpDate(fields.exp_date);
			$('#post-title').val(fields.title);
			$('#details').val(fields.details);

			_.each(this.ar,function(item){
				var jsonfield = item.jsonfield,title=item.title;
				$('#'+jsonfield+'place').html(generateTypeAhead(title, jsonfield));
				makeTagWidget(jsonfield,'/api/json/get/'+jsonfield, window.tempfields[jsonfield]);
			});
			$.noop();

		},

		initialize : function(offer){
			if(offer === false){
				this.url = '/api/json/add/market/offer';
				$('#datetimepicker1').datetimepicker({format:'D/M/YYYY HH:mm'});
				_.each(this.ar,function(item){
					$('#'+item.jsonfield+'place').html(generateTypeAhead(item.title, item.jsonfield));
					makeTagWidget(item.jsonfield,'/api/json/get/'+item.jsonfield);
				});
			}else{
				var that=this;
				this.getOffer(offer,function(offerobj){
					that.url = '/api/json/edit/market/'+offerobj[0].pk;
					that.setForm(offerobj);
				});
			}
		},

		submit: function(e){
			e.preventDefault();
			$.ajaxSetup({traditional: true});
			$.ajax({
				type: 'POST',
				url: this.url,
				dataType:'json',
				data: this.getFormData()
			});
			return false;
		}
	});

	window.offer_form = window.offer_form|| {};
	window.offer_form.initOffer = function(offer){
  		var offer_form = new OfferView(offer);
	};
})();