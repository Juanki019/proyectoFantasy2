import mysql.connector
import csv

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