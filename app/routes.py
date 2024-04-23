from flask import render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_mail import Mail, Message
from flask import session
import http.client
import json
from models.LinearRegressionModel import LinearRegressionModel
from querys.querys import cargar_datos_desde_bd, cargar_datos_jornadas_desde_bd, cargar_datos_lesionados_desde_bd, get_player_info, get_team_info, guardar_credenciales, guardar_plantilla_bd, obtener_plantilla_usuario, verificar_credenciales, update_contrasena, obtener_id_usuario_logueado
from classes.Usuario import Usuario
from telegram import Bot
from aiogram import Bot
from datetime import datetime, timedelta

routes_config = Blueprint('routes', __name__)

linear_regression_model = LinearRegressionModel()

@routes_config.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'register':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            
            nuevo_usuario = Usuario(username, password, email)
            
            if guardar_credenciales(nuevo_usuario):
                flash(f'Registro exitoso para {username}', 'success')
                await send_notification(chat_id, username)
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


@routes_config.route('/resultadosCompeticiones')
def resultadosCompeticiones():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    conn = http.client.HTTPSConnection("free-football-soccer-videos.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "2c4364d074msh916a298dace8e1bp1d5dc4jsn4ee4b76ffe0a",
        'X-RapidAPI-Host': "free-football-soccer-videos.p.rapidapi.com"
    }

    conn.request("GET", "/", headers=headers)

    res = conn.getresponse()
    if res.status == 200:
        data_api = json.loads(res.read().decode("utf-8"))
        competitions = set(objeto['competition']['name'] for objeto in data_api)
        return render_template('resultadosCompeticiones.html', players=datos_jugadores, lesiones=lesion_jugadores, data_api=data_api, competitions=competitions)
    else:
        return "Error al obtener los datos de la API"    






@routes_config.route('/datajugadores')
def datajugadores():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    jornadas = cargar_datos_jornadas_desde_bd()
    conn = http.client.HTTPSConnection("laliga-standings.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': "2c4364d074msh916a298dace8e1bp1d5dc4jsn4ee4b76ffe0a",
        'X-RapidAPI-Host': "laliga-standings.p.rapidapi.com"
    }
    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()
    if res.status == 200:
        data_api = json.loads(res.read().decode("utf-8"))
        return render_template('datajugadores.html', players=datos_jugadores, lesiones=lesion_jugadores, data_api=data_api, jornadas=jornadas)
    else:
        return "Error al obtener los datos de la API"    



@routes_config.route('/alineaciones')
def alineaciones():
    if 'username' in session:  
        print("Usuario en sesión:", session['username'])  
        usuario_actual = session['username']
        plantilla_usuario = obtener_plantilla_usuario(usuario_actual)
        datos_jugadores = cargar_datos_desde_bd()
        lesion_jugadores = cargar_datos_lesionados_desde_bd()
        
        plantilla_con_info = []
        for jugador in plantilla_usuario:
            for datos_jugador in datos_jugadores:
                if jugador == datos_jugador['Nombre']:
                    plantilla_con_info.append(datos_jugador)
                    break  # Una vez que se encuentra el jugador, se sale del bucle interno

        return render_template('alineaciones.html', players=datos_jugadores, lesiones=lesion_jugadores, plantilla=plantilla_con_info)
    
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


@routes_config.route('/predict_player', methods=['POST'])
def predict_player():
    player_name = request.json['player_name']  
    target_column = request.json['target_column']  
    
    player_data = get_player_info(player_name)
    
    datos_jugadores = cargar_datos_desde_bd()

    prediction = train_and_predict(datos_jugadores, player_data, target_column)

    # Devolver la predicción al cliente
    return jsonify({'prediction': prediction})


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


########################################################################################
#                        FUNCIONES CONFIG
########################################################################################

def train_and_predict(df, player_data, target_column):
    X = df.drop(['Nombre', 'Posicion', 'Equipo', target_column], axis=1)
    y = df[target_column]

    model = LinearRegressionModel()

    model.train(X, y)

    prediction = model.predict(player_data)
    return prediction

bot_token = '7001449113:AAGj6_iTg_uIKTc6biDIlfD_WPRUFHxCWv0'
chat_id = '1369962968'

async def send_notification(chat_id, username):
    message = f'Bienvenido a DreamXI! {username}'
    bot = Bot(bot_token)
    await bot.send_message(chat_id=chat_id, text=message)
    return 'Notificación enviada con éxito.'

async def send_notification_jornada(chat_id, jornada):
    message = f'La jornada va a comenzar, prepara tu equipo antes de que sea demasiado tarde! {jornada}'
    bot = Bot(bot_token)
    await bot.send_message(chat_id=chat_id, text=message)
    return 'Notificación enviada con éxito.'



