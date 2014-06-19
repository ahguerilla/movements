(function () {
  window.ahr = window.ahr || {};
  window.ahr.item_form_base = window.ahr.BaseView.extend({
    submit: function (e) {
      e.preventDefault();
      var that = this;
      $('#' + that.el.id + ' #itemformerror').empty();
      $('#' + that.el.id + ' .error').empty();

      var dfrd = $.ajax({
        type: 'POST',
        url: this.url,
        dataType: 'json',
        traditional: true,
        data: this.getFormData()
      });
      dfrd.done(function () {
        if (that.aftersubmit) {
          that.aftersubmit();
        }
        return true;
      });

      dfrd.fail(function (data) {
        for (var item in data.responseJSON.errors) {
          $('.' + data.responseJSON.errors[item][0] + '.error', $(that.el)).html(data.responseJSON.errors[item][1]);
          if (data.responseJSON.errors[item][0] == "__all__") {
            that.alert(data.responseJSON.errors[item][1], '#' + that.el.id + ' #itemformerror');
          }
        }
      });

      return false;
    }
  });
})();