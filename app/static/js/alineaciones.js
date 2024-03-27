var jugadores = [];
var jugadoresMC = []; 
var jugadoresDL = []; 
var jugadoresDF = []; 
var jugadoresPO = []; 
var alineacion = document.getElementById("alineacion_select");
var cmCount = 0; 
var dcCount = 0;
var poCount = 0;
var dlCount = 0;
var precioTotal = 0; 

function agregarJugador() {
    var alineacion = document.getElementById("alineacion_select").value;
    var jugadorSeleccionado = document.getElementById("player_select").value;
    var posicionJugador = document.getElementById("player_select").options[document.getElementById("player_select").selectedIndex].getAttribute('data-posicion');
    var precioJugador = parseFloat(document.getElementById("player_select").options[document.getElementById("player_select").selectedIndex].getAttribute('data-precio')); 
    var idJugador = parseFloat(document.getElementById("player_select").options[document.getElementById("player_select").selectedIndex].getAttribute('data-id')); 

    if (jugadores.some(jugador => jugador.id === idJugador)) {
        alert("Este jugador ya ha sido seleccionado.");
        return;
    }

    if (alineacion === "4-4-2") {
        if (cmCount >= 4 && esCentrocampista(posicionJugador)) {
            alert("Ya se han seleccionado 4 centrocampistas.");
            return;
        } else if (dcCount >= 4 && esDefensaCentral(posicionJugador)) {
            alert("Ya se han seleccionado 2 defensas centrales.");
            return;
        } else if (dlCount >= 2 && esDelanteroLateral(posicionJugador)) {
            alert("Ya se han seleccionado 4 defensas laterales.");
            return;
        }else if(poCount >= 1 && esPortero(posicionJugador)){
            alert("Ya se han seleccionado 1 portero.");
            return;
        }

    } else if (alineacion === "4-3-3") {
        if (cmCount >= 3 && esCentrocampista(posicionJugador)) {
            alert("Ya se han seleccionado 4 centrocampistas.");
            return;
        } else if (dcCount >= 4 && esDefensaCentral(posicionJugador)) {
            alert("Ya se han seleccionado 2 defensas centrales.");
            return;
        } else if (dlCount >= 3 && esDelanteroLateral(posicionJugador)) {
            alert("Ya se han seleccionado 3 delanteros.");
            return;
        }else if(poCount >= 1 && esPortero(posicionJugador)){
            alert("Ya se han seleccionado 1 portero.");
            return;
        }
    } else if (alineacion === "3-5-2") {
        if (cmCount >= 5 && esCentrocampista(posicionJugador)) {
            alert("Ya se han seleccionado 4 centrocampistas.");
            return;
        } else if (dcCount >= 3 && esDefensaCentral(posicionJugador)) {
            alert("Ya se han seleccionado 2 defensas centrales.");
            return;
        } else if (dlCount >= 2 && esDelanteroLateral(posicionJugador)) {
            alert("Ya se han seleccionado 4 delantero.");
            return;
        }else if(poCount >= 1 && esPortero(posicionJugador)){
            alert("Ya se han seleccionado 1 portero.");
            return;
        }
    }

// Después de agregar un jugador al array específico, llamar a actualizarListaJugadores con el array correspondiente
if (posicionJugador === "MC") {
    cmCount++;
    jugadoresMC.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador });
    actualizarListaJugadores("lista_jugadores_mc", jugadoresMC);
} else if (posicionJugador === "DF") {
    dcCount++;
    jugadoresDF.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador });
    actualizarListaJugadores("lista_jugadores_df", jugadoresDF);
} else if (posicionJugador === "PO") {
    poCount++;
    jugadoresPO.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador });
    actualizarListaJugadores("lista_jugadores_po", jugadoresPO);
} else if (posicionJugador === "DL") {
    dlCount++;
    jugadoresDL.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador });
    actualizarListaJugadores("lista_jugadores_dl", jugadoresDL);
}


    var precioTotalElement = document.getElementById("precio_total");
    var precioTotal = parseFloat(precioTotalElement.textContent);
    precioTotal += precioJugador; 
    precioTotalElement.textContent = precioTotal;

    var jugador = { nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador };
    jugadores.push(jugador);
    
    actualizarListaJugadores("lista_jugadores");
    
}

function actualizarListaJugadores(containerId, listaJugadores) {
    var listaElement = document.getElementById(containerId);
    
    listaElement.innerHTML = "";
    
    listaJugadores.forEach(function(jugador, index) {
        var listItem = document.createElement("li");
        listItem.textContent = jugador.nombre + " - " + jugador.posicion + " - "; 
        
        var btnQuitar = document.createElement("button");
        btnQuitar.textContent = "Quitar";
        
        btnQuitar.addEventListener("click", function() {
            var posicionJugadorEliminado = jugador.posicion;
    
            var precioJugadorEliminado = listaJugadores[index].precio;
            
            listaJugadores.splice(index, 1); 
            
            actualizarContadores(posicionJugadorEliminado);
            actualizarListaJugadores(containerId, listaJugadores); 
            
            precioTotal -= precioJugadorEliminado;
            
            document.getElementById("precio_total").textContent = precioTotal;
        });
        
        listItem.appendChild(btnQuitar);
        
        listaElement.appendChild(listItem);
    });
}


function actualizarContadores(posicion) {
    if (posicion === "MC") {
        cmCount--;
    } else if (posicion === "DF") {
        dcCount--;
    } else if (posicion === "PO") {
        poCount--;
    } else if (posicion === "DL") {
        dlCount--;
    }
}


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('form_guardar_plantilla').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente
        if (jugadores.length !== 11) {
            alert("Debes seleccionar exactamente 11 jugadores antes de guardar la plantilla.");
            return; 
        }
        var alineacionSelect = document.getElementById("alineacion_select");
        var alineacion = alineacionSelect.value;

        var data = {
            alineacion: alineacion,
            jugadores: jugadores.map(jugador => jugador.id), 
        };

        fetch('/guardar_plantilla', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                alert("Plantilla guardada exitosamente");
                window.location.href = "/index";
            } else {
                alert("Error al guardar la plantilla");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error al guardar la plantilla");
        });
    });
});


function esCentrocampista(posicion) {
    return posicion === "MC";
}

function esDelanteroLateral(posicion) {
    return posicion === "DL";
}

function esDefensaCentral(posicion) {
    return posicion === "DF";
}


function esPortero(posicion) {
    return posicion === "PO";
}


    function showPlayerStats() {
        // Obtener el panel de estadísticas del jugador
        var playerStatsPanel = document.getElementById("playerStatsPanel");

        // Mostrar el panel de estadísticas del jugador
        playerStatsPanel.style.display = "block";

        // Obtener los datos del jugador (puedes obtenerlos desde el botón o desde cualquier otra fuente)
        var playerName = "Nombre del Jugador"; // Reemplaza esto con el nombre real del jugador
        var playerPosition = "Posición del Jugador"; // Reemplaza esto con la posición real del jugador
        var playerPrice = "Precio del Jugador"; // Reemplaza esto con el precio real del jugador

        // Mostrar las estadísticas del jugador en el panel
        document.getElementById("playerName").innerText = playerName;
        document.getElementById("playerPosition").innerText = playerPosition;
        document.getElementById("playerPrice").innerText = playerPrice;
        // Agrega más estadísticas según sea necesario
    }
