var io = io();

function setBoxesToPlayer(player,last_move, ...boxes){
	let element = document.getElementById(last_move).classList
	element.remove(player+"Current")
	element.remove(player)
	element.add(player)
	for (const box of boxes) {
		let element = document.getElementById(box).classList;
		console.log(element);
		element.remove('neutral');
		element.add(player+"Current");
	}
}



const socket = io.connect(window.location.origin);


socket.on('connect', function() {
	//enable the arrow
});
socket.on('moveChecked',(past_move1,move_1,past_move2,move_2)=>{
  //color case if api response is a move else message
	setBoxesToPlayer('player1',`c${past_move1.y+1}r${past_move1.x+1}`,[`c${move_1.y+1}r${move_1.x+1}`])
	setBoxesToPlayer('player2',`c${past_move2.y+1}r${past_move2.x+1}`,[`c${move_2.y+1}r${move_2.x+1}`])
});

function emitMove(move){
  //disable arrow
	console.log(move)
	socket.emit('move',move);
}
function requestMoveAi(){
//socket.emit('aiMove');
}
