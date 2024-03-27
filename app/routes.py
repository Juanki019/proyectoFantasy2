from flask import render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_mail import Mail, Message
from flask import session
from querys.querys import cargar_datos_desde_bd, cargar_datos_lesionados_desde_bd, get_player_info, get_team_info, guardar_credenciales, guardar_plantilla_bd, obtener_plantilla_usuario, verificar_credenciales, update_contrasena, obtener_id_usuario_logueado
from classes.Usuario import Usuario

routes_config = Blueprint('routes', __name__)


@routes_config.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'register':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            
            nuevo_usuario = Usuario(username, password, email)
            
            if guardar_credenciales(nuevo_usuario):
                flash(f'Registro exitoso para {username}', 'success')
            else:
                flash(f'Error al registrar el usuario {username}', 'error')           
        elif action == 'login':   
            username = request.form['username']
            password = request.form['password']
            
            usuario = Usuario(username, password, None)
            
            if verificar_credenciales(usuario):
                session['username'] = username
                flash(f'Inicio de sesión exitoso para {username}')  
                return redirect(url_for('index'))
            else:
                flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
            
    return render_template('login.html')


@routes_config.route('/olvidocontrasena', methods=['GET', 'POST'])
def olvidocontrasena():
    if request.method == 'POST':
        email = request.form['email']
        msg = Message('Reset password', sender='your-email@example.com', recipients=[email])
        msg.body = 'Aquí está el enlace para restablecer tu contraseña: http://tu-sitio.com/reset_password'
        Mail.send(msg)
    return render_template('olvidoContrasena.html')


@routes_config.route('/olvidocontrasena/reiniciocontrasena', methods=['GET', 'POST'])
def reiniciocontrasena():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario = Usuario(username, password, None)

        update_contrasena(usuario)
        flash('Contraseña actualizada exitosamente', 'success')
        return redirect(url_for('login'))  # Redirigir a la página de inicio de sesión después de restablecer la contraseña
    else:
        return render_template('reinicioContrasena.html')


@routes_config.route('/index')
def index():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('index.html', players=datos_jugadores, lesiones=lesion_jugadores)

@routes_config.route('/datajugadores')
def datajugadores():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('datajugadores.html', players=datos_jugadores, lesiones=lesion_jugadores)



@routes_config.route('/alineaciones')
def alineaciones():
    if 'username' in session:  
        print("Usuario en sesión:", session['username'])  
        usuario_actual = session['username']
        plantilla_usuario = obtener_plantilla_usuario(usuario_actual)
        datos_jugadores = cargar_datos_desde_bd()
        lesion_jugadores = cargar_datos_lesionados_desde_bd()
        return render_template('alineaciones.html', players=datos_jugadores, lesiones=lesion_jugadores, plantilla=plantilla_usuario)
    else:
        flash('Debes iniciar sesión para acceder a esta página', 'error')
        return redirect(url_for('login'))  


@routes_config.route('/alineacionesProbables')
def alineacionesProbables():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('alineacionesProbables.html', players=datos_jugadores, lesiones=lesion_jugadores)


@routes_config.route('/miequipo')
def miequipo():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('miequipo.html', players=datos_jugadores, lesiones=lesion_jugadores)


@routes_config.route('/player_info')
def player_info():
    selected_player = request.args.get('player')
    player_info = get_player_info(selected_player)
    return jsonify(player_info)


@routes_config.route('/prediccion')
def prediccion():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('prediccion.html', players=datos_jugadores, lesiones=lesion_jugadores)


@routes_config.route('/guardar_plantilla', methods=['POST'])
def guardar_plantilla():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            alineacion = data.get('alineacion')
            jugadores = data.get('jugadores')
            if alineacion is not None and jugadores is not None:
                usuario_actual = obtener_id_usuario_logueado()
                if usuario_actual:
                    guardar_plantilla_bd(usuario_actual, jugadores, alineacion)
                    return jsonify({'message': 'Plantilla guardada exitosamente'}), 200
                else:
                    return jsonify({'message': 'Usuario no identificado'}), 400
            else:
                return jsonify({'message': 'Datos faltantes en la solicitud'}), 400
        else:
            return jsonify({'message': 'Solicitud no es JSON'}), 400
    else:
        return jsonify({'message': 'Método no permitido'}), 405

@routes_config.route('/team_info')
def team_info():
    selected_team = request.args.get('team')
    team_info = get_team_info(selected_team)
    return jsonify(team_info)

@routes_config.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))