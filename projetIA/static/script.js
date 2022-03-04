function setBoxesToPlayer(player, ...boxes){
	for (const box of boxes) {
		let element = document.getElementById(box).classList;
		console.log(element);
		element.remove('neutral');
		element.add(player);
	}
}

