import requests
from bs4 import BeautifulSoup
import mysql.connector
import os

def scrape_jornadas(url):
    # Realizar la solicitud HTTP al endpoint
    response = requests.get(url)
    
    if response.status_code == 200:
        # Analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Inicializar una lista para almacenar los elementos encontrados
        jornadas_info = []
        
        # Iterar sobre las jornadas
        for i in range(1, 39):  # Iterar sobre las 33 jornadas
            # Encontrar los elementos div con la clase "jornada"
            jornada_div = soup.find('div', id=f'jornada-{i}')
            if jornada_div:
                # Encontrar el elemento h2 dentro del div
                h2_element = jornada_div.find('h2', class_='tit-modulo')
                # Encontrar el elemento "a" dentro del h2
                a_element = h2_element.find('a')
                # Extraer el texto de la jornada y la URL
                jornada = a_element.text.strip()
                fecha_element = h2_element.find('span', class_='fecha-evento')
                fecha = fecha_element.text.strip()
                # Agregar la información a la lista
                jornadas_info.append((jornada, fecha))
        
                tabla_resultados = jornada_div.find('table', class_='tabla-datos')
                if tabla_resultados:
                    # Iterar sobre las filas de la tabla
                    for fila in tabla_resultados.find_all('tr'):
                        # Obtener las celdas de la fila
                        celdas = fila.find_all('td')
                        if len(celdas) == 3:  # Verificar si hay tres celdas
                            # Extraer los datos de las celdas
                            equipo_local = celdas[0].text.strip()
                            marcador = celdas[1].text.strip()
                            equipo_visitante = celdas[2].text.strip()
                            # Agregar los datos a la lista
                            jornadas_info.append((equipo_local, marcador, equipo_visitante))
        
        
        return jornadas_info
    else:
        print("Error al realizar la solicitud HTTP")
        return None


def guardar_csv(jornadas_info):
    # Nombre del archivo CSV
    nombre_archivo = "C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\data\\jornadas.csv"
    # Encabezados del archivo CSV
    encabezados = ["Jornada", "Fecha", "Equipo Local", "Marcador", "Equipo Visitante"]
    
    # Abrir el archivo CSV en modo escritura
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        # Crear el escritor CSV
        escritor_csv = csv.writer(archivo_csv)
        # Escribir los encabezados
        escritor_csv.writerow(encabezados)
        
        jornada_actual = None
        fecha_actual = None
        
        # Escribir los datos en el CSV
 
        # Escribir los datos en el CSV
        for item in jornadas_info:
            # Si el elemento es una tupla de (jornada, fecha), actualizar la jornada y la fecha actuales
            if len(item) == 2:
                jornada_actual, fecha_actual = item[0], item[1]
            # Si el elemento es una tupla de (equipo_local, marcador, equipo_visitante), escribir esos datos con la jornada y la fecha actuales
            elif len(item) == 3:
                escritor_csv.writerow([jornada_actual, fecha_actual, item[0], item[1], item[2]])


def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dreamxi",
    )
    
def guardar_en_base_dato(jornadas_info):
    # Conexión a la base de datos
    conexion = conectar_bd()
    
    try:
        with conexion.cursor() as cursor:
            # Eliminar los datos existentes en la tabla correspondiente
            cursor.execute("DELETE FROM jornadas")
            
            # Insertar los nuevos datos desde el scraper en la tabla
            for item in jornadas_info:
                # Si el elemento es una tupla de (jornada, fecha), actualizar la jornada y la fecha actuales
                if len(item) == 2:
                    jornada_actual, fecha_actual = item[0], item[1]
                # Si el elemento es una tupla de (equipo_local, marcador, equipo_visitante), insertar esos datos con la jornada y la fecha actuales
                elif len(item) == 3:
                    cursor.execute("INSERT INTO jornadas (Jornada, Fecha, Equipo_Local, Resultado, Equipo_Visitante) VALUES (%s, %s, %s, %s, %s)",
                                   (jornada_actual, fecha_actual, item[0], item[1], item[2]))
                
        # Confirmar la transacción
        conexion.commit()
        print("Los datos se han actualizado correctamente en la base de datos.")
    except Exception as e:
        # En caso de error, deshacer la transacción
        conexion.rollback()
        print(f"Error al actualizar los datos en la base de datos: {str(e)}")
    finally:
        # Cerrar la conexión
        conexion.close()

if __name__ == '__main__':  
    # URL del endpoint
    url = "https://resultados.as.com/resultados/futbol/primera/calendario/"
    # Llamar a la función para obtener la información de las jornadas
    jornadas_info = scrape_jornadas(url)
    # Si se encontraron datos de las jornadas, guardarlos en la base de datos
    if jornadas_info:
        guardar_en_base_dato(jornadas_info)
    else:
        print("No se pudieron encontrar datos de las jornadas.")