const socket = io();


// =========================
// JOGADOR
// =========================

const playerName =
    localStorage.getItem("playerName");

const playerId =
    localStorage.getItem("playerId");


document.getElementById(
    "player"
).textContent =
    "👤 " + playerName;


// =========================
// CONEXÃO
// =========================

socket.on("connect", () => {

    document.getElementById(
        "status"
    ).textContent =
        "🟢 CONECTADO";


    // Envia identidade para Python

    socket.emit(
        "player_login",
        {
            id: playerId,
            name: playerName
        }
    );

});


socket.on("disconnect", () => {

    document.getElementById(
        "status"
    ).textContent =
        "🔴 DESCONECTADO";

});


// =========================
// CONTROLE
// =========================

function sendCommand(command) {

    socket.emit(
        "controller_input",
        {
            playerId: playerId,
            playerName: playerName,

            command: command,

            timestamp: Date.now()
        }
    );

}