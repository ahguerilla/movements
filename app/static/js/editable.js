$(function(){
    $(".editablelink").hide();
    html_dialog = '<div id="editdialog" style="display:none;">Test</div>';
    $.contextMenu({
        selector:  "#"+ $(".editablelink").closest('div').attr('id'),
        trigger: 'hover',
        delay: 500,
        autoHide: true,
        callback: function(key, options) {
            //$('body').append(html_dialog);
            //$('#editdialog').dialog({});
            window.location = $('.editablelink',$(options.selector))[0].href
            },
        items: {
            "edit": {name: "Edit", icon: "edit"},
        }
    });
});
