from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
import csv
import mysql.connector


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = ''  
app.config['MAIL_PASSWORD'] = ''  

mail = Mail(app)


###########################
# FUNCIONES
###########################

# Ruta para cargar y procesar el archivo CSV
def cargar_datos_desde_csv(ruta_csv):
    with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        datos = list(lector_csv)
    return datos

# Conexión a la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dreamxi"
    )
    
# Función para cargar datos de jugadores desde la base de datos
def cargar_datos_desde_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jugadores")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos

def verificar_credenciales(username, password):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "SELECT COUNT(*) FROM usuarios WHERE user = %s AND password = %s"
    cursor.execute(query, (username, password))
    count = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    return count > 0

def guardar_credenciales(username, password, email):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "INSERT INTO usuarios (user, password, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, email))
    conexion.commit()
    cursor.close()
    conexion.close()

def update_contrasena(username, new_password):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "UPDATE usuarios SET password = %s WHERE user = %s"
    cursor.execute(query, (new_password, username))
    conexion.commit()
    cursor.close()
    conexion.close()

# Función para cargar datos de jugadores lesionados desde la base de datos
def cargar_datos_lesionados_desde_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lesiones")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos

def get_player_info(player_name):
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM jugadores WHERE Nombre = %s"
    cursor.execute(query, (player_name,))
    player_info = cursor.fetchone()
    cursor.close()
    conexion.close()
    return player_info
    
def get_team_info(team_name):
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM jugadores WHERE Equipo = %s"
    cursor.execute(query, (team_name,))
    team_info = cursor.fetchall()
    conexion.close()
    cursor.close()
    return team_info
    

###########################
# RUTAS #################################
###########################

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/olvidocontrasena', methods=['GET', 'POST'])
def olvidocontrasena():
    if request.method == 'POST':
        email = request.form['email']
        msg = Message('Reset password', sender='your-email@example.com', recipients=[email])
        msg.body = 'Aquí está el enlace para restablecer tu contraseña: http://tu-sitio.com/reset_password'
        mail.send(msg)
    return render_template('olvidoContrasena.html')

@app.route('/olvidocontrasena/reiniciocontrasena', methods=['GET', 'POST'])
def reiniciocontrasena():
    username = request.form['username']
    password = request.form['password']
    update_contrasena(username, password)
    return render_template('reinicioContrasena.html')



@app.route('/datajugadores')
def datajugadores():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('datajugadores.html', players=datos_jugadores, lesiones=lesion_jugadores)



@app.route('/alineaciones')
def alineaciones():
    datos_jugadores = cargar_datos_desde_bd()
    lesion_jugadores = cargar_datos_lesionados_desde_bd()
    return render_template('alineaciones.html', players=datos_jugadores, lesiones=lesion_jugadores)


@app.route('/alineacionesProbables')
def alineacionesProbables():
    datos_jugadores = cargar_datos_desde_csv('DATABASE/temporada2023.csv')
    lesion_jugadores = cargar_datos_desde_csv('DATABASE/lesionados.csv')
    return render_template('alineacionesProbables.html', players=datos_jugadores, lesiones=lesion_jugadores)



@app.route('/miequipo')
def miequipo():
    datos_jugadores = cargar_datos_desde_csv('DATABASE/temporada2023.csv')
    lesion_jugadores = cargar_datos_desde_csv('DATABASE/lesionados.csv')
    return render_template('miequipo.html', players=datos_jugadores, lesiones=lesion_jugadores)


@app.route('/player_info')
def player_info():
    selected_player = request.args.get('player')
    player_info = get_player_info(selected_player)
    return jsonify(player_info)


@app.route('/team_info')
def team_info():
    selected_team = request.args.get('team')
    team_info = get_team_info(selected_team)
    return jsonify(team_info)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
