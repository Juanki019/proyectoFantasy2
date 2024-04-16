document.addEventListener('DOMContentLoaded', function() {
    var showPlayerInfoButton = document.getElementById('show_player_info');
    var playerSelect = document.getElementById('player_select');
    var playerInfoDiv = document.getElementById('player_info');

    showPlayerInfoButton.addEventListener('click', function() {
        var selectedPlayer = playerSelect.value;
        fetch('/player_info?player=' + encodeURIComponent(selectedPlayer))
            .then(response => response.json())
            .then(data => {

                playerInfoDiv.innerHTML = '';

                var playerInfo = document.createElement('p');
                playerInfo.textContent = 'Nombre: ' + data.Nombre + ', Equipo: ' + data.Equipo + ', Precio: ' + data.Precio + ', Puntos: ' + data.Puntos + ', Goles: ' + data.Goles + ', Trjetas rojas: ' + data.Tarjetas_rojas + ', Tarjetas amarillas: ' + data.Tarjetas_amarillas + ', Antepenultima Jornada: ' + data.Antepenultima_Jornada + ', Penultima Jornada: ' + data.Penultima_Jornada + ', Ultima Jornada: ' + data.Ultima_Jornada + ', Tendencia: ' + data.Flecha;
                playerInfoDiv.appendChild(playerInfo);
            })
            .catch(error => console.error('Error al obtener la información del jugador:', error));
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var showPlayerInfoButton = document.getElementById('show_player_info');
    var playerSelect = document.getElementById('player_select');
    var targetSelect = document.getElementById('target_select');
    var playerInfoDiv = document.getElementById('player_info');

    showPlayerInfoButton.addEventListener('click', function() {
        var selectedPlayer = playerSelect.value;
        var selectedTarget = targetSelect.value;

        // Aquí se envía una solicitud al servidor para obtener la predicción
        fetch('/predict_player', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                player_name: selectedPlayer,
                target_column: selectedTarget
            })
        })
        .then(response => response.json())
        .then(data => {
            playerInfoDiv.innerHTML = '';

            // Muestra la predicción en el div player_info
            var predictionText = document.createElement('p');
            predictionText.textContent = 'Predicción para ' + selectedTarget + ' del jugador ' + selectedPlayer + ': ' + data.prediction;
            playerInfoDiv.appendChild(predictionText);
        })
        .catch(error => console.error('Error al obtener la predicción:', error));
    });
});
