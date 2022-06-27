function handleMove(move) {
    axios.post('http://127.0.0.1:5000/move', {
        move: move
    }).then(function (response) {
        console.log(response)
        if(response.data.status == 200){
            document.getElementsByClassName('player2Current')[0].classList.add('player2');
            document.getElementsByClassName('player2Current')[0].classList.remove('player2Current');
            for(let enclos_case of response.data.captured_position){
                document.getElementById(`c${enclos_case.x+1}r${enclos_case.y+1}`).classList.add('player2');
            }
            document.getElementById(`c${response.data.new_position.x+1}r${response.data.new_position.y+1}`).classList.add('player2Current');
            getMove();
            return;

        }
        if(response.data.status == 201){
            //redirect to result page
            window.location.href = "http://127.0.0.1:5000/result";
            return
        }
            alert("Move is wrong")

    }).catch(function (error) {
        console.log(error);
    }).then(function () {
        // always executed
    });
}

function getMove(){
    axios.get('http://127.0.0.1:5000/move').then(function (response) {
        if(response.data.status == 200){
            document.getElementsByClassName('player1Current')[0].classList.add('player1');
            document.getElementsByClassName('player1Current')[0].classList.remove('player1Current');
            for(let enclos_case of response.data.captured_position){
                document.getElementById(`c${enclos_case.x+1}r${enclos_case.y+1}`).classList.add('player1');
            }
            document.getElementById(`c${response.data.new_position.x+1}r${response.data.new_position.y+1}`).classList.add('player1Current');
        }else{
            alert("Move is wrong")
        }
    }).catch(function (error) {
        console.log(error);
    }).then(function () {
        // always executed
    });
}