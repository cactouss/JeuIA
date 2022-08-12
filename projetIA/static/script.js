async function handleMove(move) {
  try {
    const reponse = await axios.post("http://127.0.0.1:5000/move", { move });
    if (reponse.data.isFinished) {
      window.location.href = "http://127.0.0.1:5000/result";
    } else {
      updateBoardColors(
        "player2",
        reponse.data.newPosition,
        reponse.data.capturedPositions
      );
      await getMove();
    }
  } catch (err) {
    console.log(err);
    alert("wrong move");
  }
}

function updateBoardColors(player, newPosition, capturedPositions) {
  if (capturedPositions)
    capturedPositions.forEach((pos) => {
      document
        .getElementById(`c${pos.x + 1}r${pos.y + 1}`)
        .classList.add(player);
    });
  document.getElementsByClassName(player + "Current")[0].classList.add(player);
  document
    .getElementsByClassName(player + "Current")[0]
    .classList.remove(player + "Current");
  document
    .getElementById(`c${newPosition.x + 1}r${newPosition.y + 1}`)
    .classList.add(player + "Current");
}

async function getMove() {
  try {
    const reponse = await axios.get("http://127.0.0.1:5000/move");
    console.log(reponse.data);
    if (reponse.data.isFinished) {
      alert("game finished");
      window.location.href = "http://127.0.0.1:5000/"
    } else {
      updateBoardColors(
        "player1",
        reponse.data.newPosition,
        reponse.data.capturedPositions
      );
    }
  } catch (err) {
    console.log(err);
    alert("wrong move");
  }
}
