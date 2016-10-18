// json_cart=JSON.parse(localStorage.getItem('simpleCart_items'));
// props = Object.getOwnPropertyNames ( json_cart )

// for (var i = 0; i < props.length; i++) {
// 	console.log( json_cart[props[i]]);
// }

str=''
$(document).ready(function() {
	var ids=Array();
	var qty=Array();
	json_cart=JSON.parse(localStorage.simpleCart_items);
	props = Object.getOwnPropertyNames ( json_cart )
	// $('#json').val(localStorage.simpleCart_items);
	for (var i = 0; i < props.length; i++) {
		ids[i]= json_cart[props[i]].name;
		qty[i]= json_cart[props[i]].quantity;
	}

	if (ids !== undefined ) {
		console.log("no undefined")
		$('#ids').val(ids)
		$('#qty').val(qty)
		
	}else{
		console.log("undefined")
	}

	$.post('/ret_cart', {ids: ids.toString() ,qty:qty.toString()}, function(data, textStatus, xhr) {
		/*optional stuff to do after success */
		$('.carrito').html(data);
		console.log(data);
	});
});
$(function() {
// code here
});
