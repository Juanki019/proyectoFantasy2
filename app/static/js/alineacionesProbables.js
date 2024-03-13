document.addEventListener("DOMContentLoaded", function() {
    // Array de URLs de las imágenes de alineaciones
    var alineaciones = [
        "/DATABASE/partido1.png",
        "./DATABASE/partido1.png",
        "/DATABASE/partido1.png",

    ];

    var alineacionesContainer = document.querySelector('.alineaciones-container');

    alineaciones.forEach(function(url) {
        var img = document.createElement('img');
        img.src = url;
        img.classList.add('alineacion');
        alineacionesContainer.appendChild(img);

        
        // Verificar si la imagen se carga correctamente
        img.onload = function() {
            console.log('Imagen cargada correctamente:', url);
        }

        // Manejar errores de carga de imagen
        img.onerror = function() {
            console.error('Error al cargar la imagen:', url);
        }
    });
});
