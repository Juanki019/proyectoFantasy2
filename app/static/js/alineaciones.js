var jugadores = [];
var jugadoresMC = []; 
var jugadoresDL = []; 
var jugadoresDF = []; 
var jugadoresPO = []; 
var alineacion = document.getElementById("alineacion_select");
var cmCount = 0; 
var dcCount = 0;
var poCount = 0;
var dlCount = 0;var jugadores = [];
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
    jugadoresMC.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
    actualizarListaJugadores("lista_jugadores_mc", jugadoresMC);
} else if (posicionJugador === "DF") {
    dcCount++;
    jugadoresDF.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
    actualizarListaJugadores("lista_jugadores_df", jugadoresDF);
} else if (posicionJugador === "PO") {
    poCount++;
    jugadoresPO.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
    actualizarListaJugadores("lista_jugadores_po", jugadoresPO);
} else if (posicionJugador === "DL") {
    dlCount++;
    jugadoresDL.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
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
            var precioJugadorEliminado = parseFloat(jugador.precio); // Convertir a número

            // Restar el precio del jugador eliminado del precio total
            precioTotal -= precioJugadorEliminado;
            document.getElementById("precio_total").textContent = precioTotal.toFixed(2);

            listaJugadores.splice(index, 1); // Eliminar el jugador de la lista

            actualizarContadores(posicionJugadorEliminado);
            actualizarListaJugadores(containerId, listaJugadores);
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


$(document).ready(function() {
    $('#eliminarPlantillaBtn').on('click', function() {
        // Aquí haces la solicitud AJAX
        $.ajax({
            url: '/eliminar_alineacion',
            type: 'DELETE',
            success: function(response) {
                // Manejar la respuesta si es necesario
                console.log('Plantilla eliminada exitosamente');
                // Recargar la página o hacer algo más después de eliminar la plantilla
            },
            error: function(xhr, status, error) {
                // Manejar errores si es necesario
                console.error('Error al eliminar la plantilla:', error);
            }
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


    function redirectTo(endpoint) {
        window.location.href = endpoint;
    }

    function verificarEliminarPlantilla() {
        var jugadores = document.getElementsByClassName("filterDiv");
        if (jugadores.length === 0) {
            alert("No tienes jugadores en tu plantilla. Agrega jugadores antes de eliminar la plantilla.");
        } else {
            window.location.href = "/eliminar_alineacion";
        }
    }


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
            alert("Ya se han seleccionado 4 defensas.");
            return;
        } else if (dlCount >= 2 && esDelanteroLateral(posicionJugador)) {
            alert("Ya se han seleccionado 2 delanteros.");
            return;
        }else if(poCount >= 1 && esPortero(posicionJugador)){
            alert("Ya se han seleccionado 1 portero.");
            return;
        }

    } else if (alineacion === "4-3-3") {
        if (cmCount >= 3 && esCentrocampista(posicionJugador)) {
            alert("Ya se han seleccionado 3 centrocampistas.");
            return;
        } else if (dcCount >= 4 && esDefensaCentral(posicionJugador)) {
            alert("Ya se han seleccionado 4 defensas.");
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
            alert("Ya se han seleccionado 5 centrocampistas.");
            return;
        } else if (dcCount >= 3 && esDefensaCentral(posicionJugador)) {
            alert("Ya se han seleccionado 3 defensas.");
            return;
        } else if (dlCount >= 2 && esDelanteroLateral(posicionJugador)) {
            alert("Ya se han seleccionado 2 delanteros.");
            return;
        }else if(poCount >= 1 && esPortero(posicionJugador)){
            alert("Ya se han seleccionado 1 portero.");
            return;
        }
    }

// Después de agregar un jugador al array específico, llamar a actualizarListaJugadores con el array correspondiente
if (posicionJugador === "MC") {
    cmCount++;
    jugadoresMC.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
    actualizarListaJugadores("lista_jugadores_mc", jugadoresMC);
} else if (posicionJugador === "DF") {
    dcCount++;
    jugadoresDF.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
    actualizarListaJugadores("lista_jugadores_df", jugadoresDF);
} else if (posicionJugador === "PO") {
    poCount++;
    jugadoresPO.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
    actualizarListaJugadores("lista_jugadores_po", jugadoresPO);
} else if (posicionJugador === "DL") {
    dlCount++;
    jugadoresDL.push({ nombre: jugadorSeleccionado, posicion: posicionJugador, id: idJugador, precio: precioJugador });
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
            var precioJugadorEliminado = parseFloat(jugador.precio); // Convertir a número

            // Restar el precio del jugador eliminado del precio total
            precioTotal -= precioJugadorEliminado;
            document.getElementById("precio_total").textContent = precioTotal.toFixed(2);

            listaJugadores.splice(index, 1); // Eliminar el jugador de la lista

            actualizarContadores(posicionJugadorEliminado);
            actualizarListaJugadores(containerId, listaJugadores);
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


$(document).ready(function() {
    $('#eliminarPlantillaBtn').on('click', function() {
        // Aquí haces la solicitud AJAX
        $.ajax({
            url: '/eliminar_alineacion',
            type: 'DELETE',
            success: function(response) {
                // Manejar la respuesta si es necesario
                console.log('Plantilla eliminada exitosamente');
                // Recargar la página o hacer algo más después de eliminar la plantilla
            },
            error: function(xhr, status, error) {
                // Manejar errores si es necesario
                console.error('Error al eliminar la plantilla:', error);
            }
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


    function redirectTo(endpoint) {
        window.location.href = endpoint;
    }

    function verificarEliminarPlantilla() {
        var jugadores = document.getElementsByClassName("filterDiv");
        if (jugadores.length === 0) {
            alert("No tienes jugadores en tu plantilla. Agrega jugadores antes de eliminar la plantilla.");
        } else {
            window.location.href = "/eliminar_alineacion";
        }
    }

