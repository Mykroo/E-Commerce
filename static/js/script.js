json_cart=JSON.parse(localStorage.getItem('simpleCart_items'));
props = Object.getOwnPropertyNames ( json_cart )

for (var i = 0; i < props.length; i++) {
	console.log( json_cart[props[i]]);
}