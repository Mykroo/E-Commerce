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
		$('.cart-items').append(data);

		//console.log(data);
	});
	$('.cls2').click(function(event) {/* Act on the event */console.log("clicks")});

	$('.cancel_pay').on('click', function(event) {
		/* Act on the event */
		localStorage.pop('simpleCart_items');
		window.location="/";
	});

	var json=JSON.parse(localStorage.simpleCart_items);
	props = Object.getOwnPropertyNames ( json );
	var aux=new Array();
	for (var i = 0; i < props.length; i++) {
		aux.push({'id_prod':json[props[i]].name,'price':json[props[i]].price,'qty':json[props[i]].quantity}); 
	}
	$('#json').val(JSON.stringify(aux))
	
	$('.view_venta').click(function(event) {
		/* Act on the event */
		var id=$(this).attr('id').replace("venta_", '');

		// $.post()
		// console.log(id);
		$.post('/get_details', {id_ship: id}, function(data, textStatus, xhr) {
			/*optional stuff to do after success */
			var json=JSON.parse(data);
			
			$('#venta_individual').find('tbody').html("")
			for (var i = 0; i < json.length; i++) {
				
				$('#venta_individual').find('tbody').append(
					'		<tr>'+
					'			<td>'+json[i].id_prod+'</td>'+
					'			<td>'+json[i].qty+'</td>'+
					'			<td>'+json[i].price+'</td>'+
					'			<td>'+json[i].total+'</td>'+
					'		</tr>'
					);
			}
		});
		$('#venta_individual').modal('toggle');
	});

});
var close_item_car=function(){
	$(this).parent().fadeOut('slow', function(c){ });
}
var nueva_venta=function() {
	localStorage.removeItem('simsimpleCart_items');
}