(function(){

  function getpkname(data, item){
    var ar=[];
    _.each(data, function(i){
      ar.push({
        pk: i.pk,
        value: i.fields[item]
      });
    });
    return ar;
  }

  function getpklookup(data){
    var ar = {};
    _.each(data, function(item){
      ar[item.pk] = item.value;
    });
    return ar;
  }

  function getStatics(){
    var dfrd = $.Deferred();
    var dfrd1=$.ajax({url:window.ahr.app_urls.getissues,dataType:'json'});
    dfrd1.done(function(data){
      window.ahr.issues = getpkname(data,'issues');
      window.ahr.issues_lookup = getpklookup(window.ahr.issues);
      var dfrd2 = $.ajax({url:window.ahr.app_urls.getskills,dataType:'json'});
      dfrd2.done(function(data){
        window.ahr.skills = getpkname(data,'skills');
        window.ahr.skills_lookup = getpklookup(window.ahr.skills);
        var dfrd3 = $.ajax({url:window.ahr.app_urls.getcountries,dataType:'json'});
        dfrd3.done(function(data){
          window.ahr.countries = getpkname(data,'countries');
          window.ahr.countries_lookup = getpklookup(window.ahr.countries);
          dfrd.resolve();
        });
      });
    });
    return dfrd;
  }

  function getcsrf(callback){
    var dfrd = $.getJSON(window.ahr.app_urls.getcsrf, function(data){callback(data);});
    dfrd.fail(function(data){
      callback(false);
    });

  }

  function clone(obj){
    // Handle the 3 simple types, and null or undefined
    if (null === obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        var copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        var copy_a = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy_a[i] = window.ahr.clone(obj[i]);
        }
        return copy_a;
    }

    // Handle Object
    if (obj instanceof Object) {
        var copy_b = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy_b[attr] = window.ahr.clone(obj[attr]);
        }
        return copy_b;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
  }

  function expandTextarea(id){
    var $element = $(id).get(0);
    $element.addEventListener('keyup', function() {
      this.style.overflow = 'hidden';
      this.style.height = 0;
      var sh = this.scrollHeight;
      if(sh < 100){
        sh = 100;
      }
      this.style.height = sh+30 + 'px';
    }, false);
  }

  function AssignFrameHeight(id) {
    var theFrame = $('#'+id, parent.document.body);
    theFrame.height(getIframeHeight(id)-150);
  }

  function getIframeHeight(iframeName) {
    return $('body',$('#'+iframeName).contents()).height();
  }

  window.ahr = window.ahr || {};
  window.ahr.getcsrf = getcsrf;
  window.ahr.getStatics = getStatics;
  window.ahr.clone = clone;
  window.ahr.expandTextarea = expandTextarea;
  window.ahr.getIframeHeight = getIframeHeight;
  window.ahr.assignFrameHeight = AssignFrameHeight

})();