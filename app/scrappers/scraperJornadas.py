import requests
from bs4 import BeautifulSoup
import csv

def scrape_jornadas(url):
    # Realizar la solicitud HTTP al endpoint
    response = requests.get(url)
    
    if response.status_code == 200:
        # Analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Inicializar una lista para almacenar los divs encontrados
        jornadas_divs = []
        
        # Iterar sobre los números de jornada
        for i in range(1, 33):  # Suponiendo que hay 32 jornadas
            # Construir el id del div
            div_id = f"jornada-{i}"
            # Encontrar el div con el id deseado
            jornada_div = soup.find('div', id=div_id)
            # Si se encuentra el div, añadirlo a la lista
            if jornada_div:
                jornadas_divs.append(jornada_div)
        
        return jornadas_divs
    else:
        print("Error al realizar la solicitud HTTP")
        return None

def guardar_csv(jornadas_divs):
    # Nombre del archivo CSV
    nombre_archivo = "C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\data\\jornadas.csv"
    # Encabezados del archivo CSV
    encabezados = ["Jornada", "Contenido"]
    
    # Abrir el archivo CSV en modo escritura
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        # Crear el escritor CSV
        escritor_csv = csv.writer(archivo_csv)
        # Escribir los encabezados
        escritor_csv.writerow(encabezados)
        
        # Iterar sobre los divs de jornadas y escribirlos en el CSV
        for i, jornada_div in enumerate(jornadas_divs, start=1):
            # Obtener el contenido del div
            contenido = jornada_div.text.strip()
            # Escribir la fila en el CSV
            escritor_csv.writerow([f"Jornada {i}", contenido])

# URL del endpoint
url = "https://resultados.as.com/resultados/futbol/primera/calendario/"
# Llamar a la función para obtener los divs de las jornadas
jornadas_divs = scrape_jornadas(url)
# Si se encontraron divs de jornadas, guardarlos en un archivo CSV
if jornadas_divs:
    guardar_csv(jornadas_divs)
    print("Los datos se han guardado correctamente en el archivo CSV.")
else:
    print("No se pudieron encontrar divs de jornadas.")
