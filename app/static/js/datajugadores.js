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
                playerInfo.textContent = 'Nombre: ' + data.Nombre + ', Equipo: ' + data.Equipo + ', Precio: ' + data.Precio + ', Puntos: ' + data.Puntos + ', Goles: ' + data.Goles;
                playerInfoDiv.appendChild(playerInfo);
            })
            .catch(error => console.error('Error al obtener la información del jugador:', error));
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var showTeamInfoButton = document.getElementById('show_team_info');
    var teamSelect = document.getElementById('team_select');
    var teamInfoDiv = document.getElementById('team_info');

    showTeamInfoButton.addEventListener('click', function() {
        var selectedTeam = teamSelect.value;
        fetch('/team_info?team=' + encodeURIComponent(selectedTeam))
            .then(response => response.json())
            .then(data => {

                teamInfoDiv.innerHTML = '';

                data.forEach(function(player) {
                    var playerInfo = document.createElement('p');
                    playerInfo.textContent = 'Nombre: ' + player.Nombre + ', Equipo: ' + player.Equipo + ', Precio: ' + player.Precio + ', Puntos: ' + player.Puntos + ', Goles: ' + player.Goles;

                    teamInfoDiv.appendChild(playerInfo);
                });
            })
            .catch(error => console.error('Error al obtener la información del jugador:', error));
    });

});

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('lesionados_chart').getContext('2d');
    var teamSelect = document.getElementById('team_select');
    
    var equipos = [];
    var cantidadLesionados = [];
    var options = teamSelect.options;
    for (var i = 0; i < options.length; i++) {
        var equipo = options[i].value;
        var lesionados = parseInt(options[i].getAttribute('data-lesiones'));
        equipos.push(equipo);
        cantidadLesionados.push(lesionados);
    }

    // Crear el gráfico de barras
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: equipos,
            datasets: [{
                label: 'Cantidad de Lesionados por Equipo',
                data: cantidadLesionados,
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color para los barras
                borderColor: 'rgba(255, 99, 132, 1)', // Color para los bordes de las barras
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // Ajuste la configuración de la escala del eje Y aquí
                }
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('search_input');
    var table = document.getElementById('jugadores-table');
    var rows = table.getElementsByTagName('tr');

    searchInput.addEventListener('keyup', function() {
        var searchText = searchInput.value.toLowerCase();

        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            var playerName = row.cells[0].textContent.toLowerCase(); 

            // Comparar el nombre del jugador con el texto de búsqueda
            if (playerName.includes(searchText)) {
                row.style.display = ''; 
            } else {
                row.style.display = 'none'; 
            }
        }
    });
});

