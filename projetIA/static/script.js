var io = io();

function setBoxesToPlayer(player, ...boxes){
	for (const box of boxes) {
		let element = document.getElementById(box).classList;
		console.log(element);
		element.remove('neutral');
		element.add(player);
	}
}



const socket = io.connect(window.location.origin);


socket.on('connect', function() {
	//enable the arrow
});
socket.on('moveChecked',(move)=>{
  //color case if api response is a move else message
	setBoxesToPlayer('player1',[`c${move.y+1}r${move.x+1}`])
});

function emitMove(move){
  //disable arrow
	console.log(move)
	socket.emit('move',move);
}
function requestMoveAi(){
//socket.emit('aiMove');
}
