from flask import render_template, request, redirect, url_for, session, flash, jsonify, Blueprint
from flask_mail import Mail, Message

from querys.querys import cargar_datos_desde_bd, cargar_datos_lesionados_desde_bd, guardar_credenciales, verificar_credenciales


routes_config = Blueprint('routes', __name__)


@routes_config.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'register':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            guardar_credenciales(username, password, email)
            print(f'Registro exitoso para {username}')  
        elif action == 'login':   
            username = request.form['username']
            password = request.form['password']
            
            if verificar_credenciales(username, password):
                session['username'] = username
                print(f'Inicio de sesión exitoso para {username}')  
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
    username = request.form['username']
    password = request.form['password']
    update_contrasena(username, password)
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
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('alineaciones.html', players=datos_jugadores, lesiones=lesion_jugadores)


@routes_config.route('/alineacionesProbables')
def alineacionesProbables():
    datos_jugadores = cargar_datos_desde_csv('DATABASE/temporada2023.csv')
    lesion_jugadores = cargar_datos_desde_csv('DATABASE/lesionados.csv')
    return render_template('alineacionesProbables.html', players=datos_jugadores, lesiones=lesion_jugadores)



@routes_config.route('/miequipo')
def miequipo():
    datos_jugadores = cargar_datos_desde_csv('DATABASE/temporada2023.csv')
    lesion_jugadores = cargar_datos_desde_csv('DATABASE/lesionados.csv')
    return render_template('miequipo.html', players=datos_jugadores, lesiones=lesion_jugadores)


@routes_config.route('/player_info')
def player_info():
    selected_player = request.args.get('player')
    player_info = get_player_info(selected_player)
    return jsonify(player_info)


@routes_config.route('/team_info')
def team_info():
    selected_team = request.args.get('team')
    team_info = get_team_info(selected_team)
    return jsonify(team_info)



@routes_config.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))