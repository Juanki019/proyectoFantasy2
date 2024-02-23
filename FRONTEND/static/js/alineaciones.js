function agregarJugador() {
    var jugadorSeleccionado = document.getElementById("player_select").value;
    
    if (jugadores.includes(jugadorSeleccionado)) {
        alert("Este jugador ya ha sido seleccionado.");
        return; 
    }

    jugadores.push(jugadorSeleccionado);
    
    actualizarListaJugadores();
}

function actualizarListaJugadores() {
    var listaJugadores = document.getElementById("lista_jugadores");
    
    listaJugadores.innerHTML = "";
    
    jugadores.forEach(function(jugador, index) {
        var listItem = document.createElement("li");
        listItem.textContent = jugador;
        
        var btnQuitar = document.createElement("button");
        btnQuitar.textContent = "Quitar";
        
        btnQuitar.addEventListener("click", function() {
            jugadores.splice(index, 1); 
            actualizarListaJugadores(); 
        });
        
        listItem.appendChild(btnQuitar);
        
        listaJugadores.appendChild(listItem);
    });
}


function guardarPlantilla() {
    if (jugadores.length !== 11) {
        alert("Debes seleccionar exactamente 11 jugadores antes de guardar la plantilla.");
        return; // No permitir guardar si no hay exactamente 11 jugadores
    }
    
}

var jugadores = [];