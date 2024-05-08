function modificarUsuario(button) {
    var fila = button.closest('tr');
    var inputs = fila.querySelectorAll('input');
    var spans = fila.querySelectorAll('span');
    var botonModificar = fila.querySelector('button');

    // Toggle entre mostrar campos de entrada y mostrar texto
    inputs.forEach(input => {
        input.style.display = input.style.display === 'none' ? 'inline' : 'none';
    });
    spans.forEach(span => {
        span.style.display = span.style.display === 'none' ? 'inline' : 'none';
    });

    // Cambiar texto del botón
    botonModificar.textContent = botonModificar.textContent === 'Modificar' ? 'Guardar' : 'Modificar';

    if (botonModificar.textContent === 'Modificar') {
        // Aquí puedes enviar los datos modificados al endpoint si lo deseas
        var idUsuario = fila.getAttribute('data-id');
        var usuario = inputs[0].value;
        var password = inputs[1].value;
        var email = inputs[2].value;
        var profile = inputs[3].value;

        fetch('/tu-endpoint-de-actualizacion', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_usuario: idUsuario,
                user: usuario,
                password: password,
                email: email,
                profile: profile
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al actualizar usuario');
            }
            alert('Usuario actualizado correctamente');
            // Aquí puedes realizar alguna acción adicional si lo deseas, como actualizar la tabla o recargar la página
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al actualizar el usuario');
        });
    }
}