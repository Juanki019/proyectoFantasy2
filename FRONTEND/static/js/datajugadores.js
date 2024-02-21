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
                    // Crear un elemento de párrafo para mostrar la información del jugador
                    var playerInfo = document.createElement('p');
                    playerInfo.textContent = 'Nombre: ' + player.Nombre + ', Equipo: ' + player.Equipo + ', Precio: ' + player.Precio + ', Puntos: ' + player.Puntos + ', Goles: ' + player.Goles;

                    // Agregar el elemento de párrafo al contenedor de información del equipo
                    teamInfoDiv.appendChild(playerInfo);
                });
            })
            .catch(error => console.error('Error al obtener la información del jugador:', error));
    });
});
