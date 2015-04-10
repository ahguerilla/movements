(function (global) {

  var CreatePostView = Backbone.View.extend({
    events: {
      'click .select-checkbox': 'checkClick',
      'submit': 'submitForm'
    },
    initialize: function() {
      this.fallback = false;
      var that = this;
      this.dz = new Dropzone(this.el, {
        paramName: "images",
        url: document.location.pathname,
        maxFilesize: 2, // MB
        uploadMultiple: true,
        autoProcessQueue: false,
        clickable: '.dz-clickable',
        previewsContainer: '.dz-preview-container',
        acceptedFile: "image/png,image/jpg,image/jpeg",
        //forceFallback: true,
        fallback: function () {
          that.$el.find('.fallback').show();
          that.$el.find('.dz-clickable,.dz-preview').hide();
          that.fallback = true;
        },
        addRemoveLinks: true
      });
    },
    checkClick: function(ev) {
      $(ev.currentTarget).find('input[type="checkbox"]').prop("checked", !$(ev.currentTarget).find('input[type="checkbox"]').prop("checked"));
      $(ev.currentTarget).toggleClass("checked");
    },
    submitForm: function(ev) {
      if (this.fallback) return;
      ev.preventDefault();
      var formData = new FormData(this.$el.get(0));
      _.each(this.dz.files, function(file, ix) {
        formData.append('image-' + ix, file);
      }, this);
      $.ajax({
        type: 'post',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(resp) {
        }
      });
    }
  });

  global.ahr.initCreatePost = function() {
    new CreatePostView({el: '#create-post-form'});
  };

})(window);
