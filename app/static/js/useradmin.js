$(document).ready(function(){  
    $('body').on('click','.sendvettedemail',function(ev){
        ev.preventDefault();
        if(confirm('Send a vetted email to this user?')){
            $.getJSON(ev.currentTarget.href,function(data){
                alert(data.message);
            });
        }
        return false;
    });
});