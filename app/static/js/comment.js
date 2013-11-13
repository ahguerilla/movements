(function(){

	var CommentView = Backbone.View.extend({
		el: '#commentform',
		events:{
				'submit' : 'submit',
  		},

		getFormData: function(){
			return {
					"title": $('#comment-title').val(),
					"contents": tinyMCE.get('id_contents').getContent(),
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				}
		},

		getComment: function(coment,func){
			this.comment=$.getJSON('/api/json/get/comment/'+coment, func);
		},


		setForm: function(data){
			tinyMCE.get('id_contents').setContent(data[0].fields.contents, {format : 'bbcode'});
			$('#comment-title').val(data[0].fields.title);
		},

		initialize : function(coment,obj_type,obj_id){
			if(coment === false){
				this.url = '/api/json/add/comment/'+obj_type+'/'+obj_id;
			}else{
				var that=this;
				this.getComment(coment.id,function(comment_obj){
					that.url = '/api/json/edit/comment/'+comment_obj[0].pk;
					that.setForm(comment_obj);
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

	window.comment = window.comment|| {};
	window.comment.initComment = function(coment,obj_type,obj_id){
  		var comment = new CommentView(coment,obj_type, obj_id);
	};
})();