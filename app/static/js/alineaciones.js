var jugadores = [];
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

    if (jugadores.includes(jugadorSeleccionado)) {
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
    if (posicionJugador === "MC") {
        cmCount++;
    } else if (posicionJugador === "DF") {
        dcCount++;
    } else if (posicionJugador === "PO") {
        poCount++;
    } else if (posicionJugador === "DL") {
        dlCount++;
    }

    var precioTotalElement = document.getElementById("precio_total");
    var precioTotal = parseFloat(precioTotalElement.textContent);
    precioTotal += precioJugador; 
    precioTotalElement.textContent = precioTotal;

    var jugador = { nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador };
    jugadores.push(jugador);
    
    actualizarListaJugadores();
}

function actualizarListaJugadores() {
    var listaJugadores = document.getElementById("lista_jugadores");
    
    listaJugadores.innerHTML = "";
    
    jugadores.forEach(function(jugador, index) {
        var listItem = document.createElement("li");
        listItem.textContent = jugador.nombre + " - " + jugador.posicion + " - "; 
        
        var btnQuitar = document.createElement("button");
        btnQuitar.textContent = "Quitar";
        
        btnQuitar.addEventListener("click", function() {
            var posicionJugadorEliminado = document.getElementById("player_select").options[index].getAttribute('data-posicion');
            var precioJugadorEliminado = parseFloat(document.getElementById("player_select").options[index].getAttribute('data-precio')); // Obtener el precio del jugador eliminado
            jugadores.splice(index, 1); 
            actualizarContadores(posicionJugadorEliminado);
            actualizarListaJugadores(); 
            precioTotal -= precioJugadorEliminado; // Restar el precio del jugador eliminado del precio total
            document.getElementById("precio_total").textContent = precioTotal; // Actualizar el precio total en el HTML

        });
        
        listItem.appendChild(btnQuitar);
        
        listaJugadores.appendChild(listItem);
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