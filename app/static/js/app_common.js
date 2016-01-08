(function () {
  function expandTextarea(id) {
    var $element = $(id).get(0);
    $element.addEventListener('keyup', function () {
      this.style.overflow = 'hidden';
      this.style.height = 0;
      var sh = this.scrollHeight;
      if (sh < 100) {
        sh = 100;
      }
      this.style.height = sh + 30 + 'px';
    }, false);
  }
  function alert(message, selector) {
    $(selector).empty();
    $(selector).prepend('<div class="alert alert-warning alert-dismissable">' +
      '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
      message + '</div>');
  }
  function clearalert(selector) {
    $(selector).empty();
  }
  function addCommasToNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
  $.fn.clickUrl = function() {
    var regexp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/i;
    this.each(function() {
        $(this).html(
          $(this).html().replace(regexp,'<a href="$1" target="_blank">$1</a>')
        );
    });
    return $(this);
  };

  window.ahr = window.ahr || {};
  window.ahr.alert = alert;
  window.ahr.clearalert = clearalert;
  window.ahr.expandTextarea = expandTextarea;
  window.ahr.addCommasToNumber = addCommasToNumber;

})();
