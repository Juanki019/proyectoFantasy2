import mysql.connector
import csv
from flask import jsonify, session, flash
from sshtunnel import SSHTunnelForwarder


def cargar_datos_desde_csv(ruta_csv):
    with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        datos = list(lector_csv)
    return datos

local_port = 35024

tunnel = SSHTunnelForwarder(
    ('195.235.211.197', 35024),
    ssh_username='ubuntu',
    ssh_password='grupo5',
    remote_bind_address=('127.0.0.1', 3306),
    local_bind_address=('0.0.0.0', local_port)
)

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="dreamxi",
        port=local_port
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

def cargar_datos_usuarios():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos

################################
# QUERYS PARA LOGIN
################################    

def is_admin_profile(usuario):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "SELECT profile FROM usuarios WHERE user = %s"
    cursor.execute(query, (usuario,))
    profile = cursor.fetchone()[0]  
    cursor.close()
    conexion.close()
    return profile

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


def guardar_credenciales_sin_contrasena(usuario):
    if verificar_existencia_usuario(usuario):
        flash(f"El nombre de usuario '{usuario.username}' ya existe en la base de datos.")
        return False  
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = "INSERT INTO usuarios (user, email) VALUES (%s, %s)"
        cursor.execute(query, (usuario.username, usuario.email))
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        print(f"Error al guardar el usuario: {e}")
        flash(f"El nombre de usuario '{usuario.username}' ya existe en la base de datos.")
        return False  

def update_contrasena(usuario):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "UPDATE usuarios SET password = %s WHERE email = %s"
    cursor.execute(query, (usuario.password, usuario.email))
    conexion.commit()
    cursor.close()
    conexion.close()

def update_usuario(user, password, email, profile, id_usuario):
    try: 
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = "UPDATE usuarios SET user=%s, password=%s, email=%s, profile=%s WHERE id_usuario=%s"
        cursor.execute(query, (user, password, email, profile, id_usuario))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {'message': 'Usuario actualizado correctamente'}
    except Exception as e:
        print(e)
        return {'error': 'Error al actualizar usuario'}

def contar_jugadores_plantilla(id_usuario):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "SELECT COUNT(*) FROM plantillas WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    cantidad = cursor.fetchone()[0]  # Obtiene el resultado del conteo
    cursor.close()
    conexion.close()
    return cantidad


################################
# QUERYS PARA CARGA DE DATOS
################################  

def cargar_datos_lesionados_desde_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lesiones")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def cargar_datos_jornadas_desde_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jornadas")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def cargar_datos_jornadas_no_jugadas_desde_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jornadas WHERE Resultado NOT LIKE '%-%'")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos

def eliminar_usuario(id_usuario):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    query = "DELETE FROM usuarios WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_plantilla_por_usuario(username):
    # Realizar la consulta para obtener el ID de usuario
    query_id_usuario = "SELECT id_usuario FROM usuarios WHERE user = %s"
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute(query_id_usuario, (username,))
    row = cursor.fetchone()
    if row:
        user_id = row[0]  # Obtener el ID de usuario de la fila
        
        # Eliminar la plantilla asociada al usuario
        cursor.execute("DELETE FROM plantilla WHERE id_usuario = %s", (user_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True  # Indicar que la eliminación fue exitosa
    else:
        cursor.close()
        conexion.close()
        return False  # Indicar que no se encontró el usuario


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

def obtener_formacion_plantilla_usuario(user):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Obtener el ID del usuario
        query_id_usuario = "SELECT id_usuario FROM usuarios WHERE user = %s"
        cursor.execute(query_id_usuario, (user,))
        id_usuario = cursor.fetchone()

        if id_usuario:
            id_usuario = id_usuario[0]  # Obtener el valor del ID del usuario

            # Obtener la formación de la plantilla del usuario utilizando su ID
            query_plantilla = """
                SELECT tipo_alineacion
                FROM plantilla
                WHERE id_usuario = %s
                LIMIT 1
            """
            cursor.execute(query_plantilla, (id_usuario,))
            plantilla = cursor.fetchone()

            if plantilla:
                print("El usuario tiene una plantilla asociada en la base de datos.")
                formacion = plantilla[0]
            else:
                print("El usuario no tiene una plantilla asociada en la base de datos.")
                formacion = None

            cursor.close()
            conexion.close()

            return formacion
        else:
            print("No se encontró el usuario en la base de datos.")
            return None
    except Exception as e:
        print(f"Error al obtener la plantilla del usuario: {e}")
        return None

def obtener_plantilla_usuario(user):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Obtener el ID del usuario
        query_id_usuario = "SELECT id_usuario FROM usuarios WHERE user = %s"
        cursor.execute(query_id_usuario, (user,))
        id_usuario = cursor.fetchone()

        if id_usuario:
            id_usuario = id_usuario[0]  # Obtener el valor del ID del usuario

            # Obtener la plantilla del usuario utilizando su ID
            query_plantilla = """
                SELECT j.Nombre
                FROM plantilla p
                JOIN jugadores j ON p.id_jugador = j.id_jugador
                WHERE p.id_usuario = %s
            """
            cursor.execute(query_plantilla, (id_usuario,))
            plantilla = cursor.fetchall()

            if plantilla:
                print("El usuario tiene una plantilla asociada en la base de datos.")
            else:
                print("El usuario no tiene una plantilla asociada en la base de datos.")

            cursor.close()
            conexion.close()

            return [row[0] for row in plantilla]
        else:
            print("No se encontró el usuario en la base de datos.")
            return []
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
    
def cargar_datos_todos_los_jugadores():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT Puntos, Precio, Media, Partidos, Minutos, Goles, Asistencias, Asistencias_sin_gol, Regates, Tiros_a_puerta, Tarjetas_rojas, Tarjetas_amarillas FROM jugadores")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos

def cargar_datos_jugador_por_nombre(nombre_jugador):
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT Puntos, Precio, Media, Partidos, Minutos, Goles, Asistencias, Asistencias_sin_gol, Regates, Tiros_a_puerta, Tarjetas_rojas, Tarjetas_amarillas FROM jugadores WHERE nombre = %s", (nombre_jugador,))
    datos = cursor.fetchone()
    cursor.close()
    conexion.close()
    return datos

