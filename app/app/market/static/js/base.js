(function(){
    setInterval(function(){
        $.getJSON(window.ahr.app_urls.getmessagecount,function(data){
            $('.message-counter').each(function(tmp,item){
                var text = $(item).text()
                var ind = text.indexOf('(');
                var txt = text.slice(0,ind+1);
                if(ind>-1){
                    $(item).text(txt+data+")");
                }
            });
        });
    }
    ,30000);
})();
