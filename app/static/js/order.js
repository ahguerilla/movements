$(function(){

  $(".module").on('click',"#moveup",function(e){
    e.preventDefault();
    var dfrd = $.ajax({
      url:e.target.href
    });
    dfrd.done(function(){
      location.reload();
    });
  });

  $(".module").on('click',"#movedown",function(e){
    e.preventDefault();
    var dfrd = $.ajax({
      url: e.target.href
    });
    dfrd.done(function(){
      location.reload();
    });
  });
});

