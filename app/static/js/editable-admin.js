$(function(){

    var a = $('#id_content');
    if(a.length>0){
        var dfrd = $.ajax({
            url:'/editable/get_images/',
            dataType: 'html'
        });
        dfrd.done(function(data){
            var html = ['<div><button id="insertimage">Insert Image</button></div>',
            '<div id="imagedialog" title="Select an image" hidden>',
            '<p>'+data+'</p></div>',
            ].join('');
            a.before(html);
            $('#insertimage').on('click',function(e){
                e.preventDefault();
                $('#imagedialog').dialog({'width':'600'});
            });
            $('.selectableimage').on('click',function(){
                $('#id_content').val($(this).attr('path'));
                $('#id_noinline').prop('checked',true);
                $('#imagedialog').dialog('close');
            });
        });

    }


});