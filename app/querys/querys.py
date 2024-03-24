import mysql.connector
import csv
from flask import session, flash


def cargar_datos_desde_csv(ruta_csv):
    with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        datos = list(lector_csv)
    return datos

"""
# Conexión a la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="195.235.211.197",
        port="35024",
        user="root",
        password="grupo5",
        database="dreamxi"
    )
"""
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

################################
# QUERYS PARA LOGIN
################################    

def verificar_existencia_usuario(usuario):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "SELECT COUNT(*) FROM usuarios WHERE user = %s"
    cursor.execute(query, (usuario.username,))
    count = cursor.fetchone()[0]  
    cursor.close()
    conexion.close()
    return count > 0

def verificar_credenciales(usuario):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "SELECT COUNT(*) FROM usuarios WHERE user = %s AND password = %s"
    cursor.execute(query, (usuario.username, usuario.password))
    count = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    return count > 0


def guardar_credenciales(usuario):
    if verificar_existencia_usuario(usuario):
        flash(f"El nombre de usuario '{usuario.username}' ya existe en la base de datos.")
        return False  
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = "INSERT INTO usuarios (user, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (usuario.username, usuario.password, usuario.email))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True  
    except Exception as e:
        print(f"Error al guardar el usuario: {e}")
        flash(f"El nombre de usuario '{usuario.username}' ya existe en la base de datos.")
        return False  


def update_contrasena(usuario):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "UPDATE usuarios SET password = %s WHERE user = %s"
    cursor.execute(query, (usuario.password, usuario.username))
    conexion.commit()
    cursor.close()
    conexion.close()

def cargar_datos_lesionados_en_bd(csv_lesionados):
    with open(csv_lesionados, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        datos_nuevos = [dict(row) for row in reader]
    
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    
    cursor.execute("DELETE FROM lesiones")
    
    for dato in datos_nuevos:
        cursor.execute("INSERT INTO lesiones (equipo, jugador, lesion) VALUES (%s, %s, %s)",
        (dato['Equipo'], dato['Jugador'], dato['Lesion']))

    conexion.commit()
    cursor.close()
    conexion.close()
    return "Datos cargados exitosamente en la base de datos."


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

def guardar_plantilla_bd(id_usuario, id_jugadores, alineacion):
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    query = "INSERT INTO plantilla (id_usuario, id_jugador, tipo_alineacion) VALUES (%s, %s, %s)"
    for id_jugador in id_jugadores:
        cursor.execute(query, (id_usuario, id_jugador, alineacion))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_id_usuario_logueado():
    usuario_actual = session.get('username')
    if usuario_actual:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = "SELECT id_usuario FROM usuarios WHERE user = %s"
        cursor.execute(query, (usuario_actual,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if resultado:
            return resultado[0]  
    return None

def update_contrasena(user, new_password):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "UPDATE usuarios SET password = %s WHERE user = %s"
    cursor.execute(query, (new_password, user))
    conexion.commit()
    cursor.close()
    conexion.close()


def obtener_plantilla_usuario(user):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = "SELECT id_jugador FROM plantillas WHERE id_usuario = (SELECT id_usuario FROM usuarios WHERE user = %s)"
        cursor.execute(query, (user,))
        plantilla = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [{'id_plantilla': row[0], 'id_usuario': row[1], 'id_jugador': row[2], 'tipo_alineacion': row[3]} for row in plantilla]
    except Exception as e:
        print(f"Error al obtener la plantilla del usuario: {e}")
        return []


def actualizar_plantilla(user, nueva_plantilla):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        # Eliminar la plantilla actual del usuario
        cursor.execute("DELETE FROM plantillas WHERE id_usuario = %s", (user,))
        # Insertar la nueva plantilla
        for jugador in nueva_plantilla:
            cursor.execute("INSERT INTO plantillas (id_usuario, id_jugador, tipo_alineacion) VALUES (%s, %s, %s)",
                            (user, jugador['id_jugador'], jugador['tipo_alineacion']))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True  
    except Exception as e:
        print(f"Error al actualizar la plantilla: {e}")
        return False
