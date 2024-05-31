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
    $('#target_select').change(function() {
        var selectedTarget = $(this).val();
        $.ajax({
            url: '/train',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({target_column: selectedTarget}),  
            success: function(response) {
                $('#trainResponse').html('Aplicación lista para predecir su dato');
            },
            error: function() {
                $('#trainResponse').html('Error en el entrenamiento del modelo.');
            }
        });
    });

    $('#predict_button').click(function() {
        var player = $('#player_select').val();  
        var target = $('#target_select').val(); 
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({player_name: player, target_column: target}),
            success: function(response) {
                if (response.prediction) {
                    $('#prediction_result').html('Prediccion para ' + response.player_name + ' --> '+ target + ': ' + response.prediction);
                } else {
                    $('#prediction_result').html('No prediction available.');
                }
            },
            error: function() {
                $('#prediction_result').html('Error retrieving prediction.');
            }
        });
    });
});

