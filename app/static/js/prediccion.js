document.addEventListener('DOMContentLoaded', function() {
    $('#target_select').change(function() {
        var selectedTargets = ['Precio', 'Goles', 'Puntos']; // Array con los nombres de las variables objetivo
        $('#trainResponse').empty(); // Limpiar cualquier mensaje anterior

        // Iterar sobre las variables objetivo y realizar una solicitud AJAX para cada una
        selectedTargets.forEach(function(target) {
            $.ajax({
                url: '/train',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ target_column: target }),  
                success: function(response) {
                    $('#trainResponse').append('<p>Modelo entrenado correctamente para ' + target + '</p>');
                    mostrarPredicciones(target); // Llamar a la función para mostrar las predicciones
                },
                error: function() {
                    $('#trainResponse').append('<p>Error en el entrenamiento del modelo para ' + target + '</p>');
                }
            });
        });
    });

    $('#predict_button').click(function() {
        var player = $('#player_select').val();  
        var target = $('#target_select').val(); 
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ player_name: player, target_column: target }),
            success: function(response) {
                if (response.prediction) {
                    $('#prediction_result').html('Predicción para ' + response.player_name + ' --> ' + target + ': ' + response.prediction);
                } else {
                    $('#prediction_result').html('No hay predicción disponible para ' + response.player_name + ' y ' + target);
                }
            },
            error: function() {
                $('#prediction_result').html('Error al recuperar la predicción.');
            }
        });
    });

    // Función para mostrar las predicciones
    function mostrarPredicciones(target) {
        // Obtener el jugador seleccionado y la variable objetivo
        var player = $('#player_select').val();  
        // Realizar la solicitud AJAX para obtener la predicción para el jugador y la variable objetivo actual
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ player_name: player, target_column: target }),
            success: function(response) {
                if (response.prediction) {
                    $('#prediction_result').append('<p>Predicción para ' + response.player_name + ' --> ' + target + ': ' + response.prediction + '</p>');
                } else {
                    $('#prediction_result').append('<p>No hay predicción disponible para ' + response.player_name + ' y ' + target + '</p>');
                }
            },
            error: function() {
                $('#prediction_result').append('<p>Error al recuperar la predicción para ' + target + '</p>');
            }
        });
    }
});
