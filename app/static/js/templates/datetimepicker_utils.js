function setDateTimePicker(item,preval){	
	if(preval){														
		$('#'+item.jsonfield).val(preval.slice(8,10)+'/'+
				preval.slice(5,7)+'/'+
				preval.slice(0,4)+' '+
				preval.slice(11,13)+':'+
				preval.slice(14,16)
			);
	}
}

function afterDateTimePicker(item){
	$('#'+item.type+'-'+item.jsonfield).datetimepicker({format:'D/M/YYYY HH:mm'});
}