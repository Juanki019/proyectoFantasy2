function modificarUsuario(button) {
    var fila = button.closest('tr');
    var inputs = fila.querySelectorAll('input');
    var selects = fila.querySelectorAll('select');
    var spans = fila.querySelectorAll('span');
    var botonModificar = fila.querySelector('button');

    // Toggle entre mostrar campos de entrada y mostrar texto
    inputs.forEach(input => {
        input.style.display = input.style.display === 'none' ? 'inline' : 'none';
    });
    selects.forEach(select => {
        select.style.display = select.style.display === 'none' ? 'inline' : 'none';
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
        var profile = selects[0].value; // Obtener el valor seleccionado del <select>

        console.log('Datos a enviar:', {
            id_usuario: idUsuario,
            user: usuario,
            password: password,
            email: email,
            profile: profile
        });

        fetch('/update_usuario', {
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
            return response.json();
        })
        .then(data => {
            alert('Usuario actualizado correctamente');
            // Recargar la página después de actualizar el usuario
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al actualizar el usuario');
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.eliminar-usuario').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const row = this.closest('tr');
            const profile = row.querySelector('td:nth-child(5) span').textContent; // Obtiene el perfil del usuario

            if (profile === '777') {
                alert('No se puede eliminar un usuario con el perfil 777.');
                return; // Sale de la función si el perfil es 777
            }
            if (confirm('¿Está seguro de que desea eliminar este usuario?')) {
                fetch('/eliminar_usuario', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id_usuario: id }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        // Elimina la fila de la tabla
                        const row = this.closest('tr');
                        row.remove();
                        alert(data.message);
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Hubo un error al eliminar el usuario.');
                });
            }
        });
    });
});
