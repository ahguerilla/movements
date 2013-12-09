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
    $.getJSON(window.ahr.app_urls.getcsrf, function(data){callback(data);});
  }

  window.ahr = window.ahr || {};
  window.ahr.getcsrf = getcsrf;
  window.ahr.getStatics = getStatics;

})();