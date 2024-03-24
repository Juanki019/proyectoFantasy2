import requests
from bs4 import BeautifulSoup
import csv

# URL de la página
url = "https://www.analiticafantasy.com/la-liga/alineaciones-probables"

# Realizar la solicitud GET a la URL
response = requests.get(url)

# Comprobar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Analizar el contenido HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar el elemento utilizando el XPath
    xpath = "/html/body/div[2]/section/section[2]/main/section/div/div/div[1]/div[1]/div/div[1]/div/div[1]"
    elemento = soup.find("div", xpath=xpath)
    
    # Verificar si se encontró el elemento
    if elemento:
        # Extraer el texto dentro del elemento
        contenido = elemento.get_text(strip=True)
        
        # Especificar la ruta del archivo CSV
        ruta_archivo_csv = 'C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\data\\jornadaX.csv'  # Cambia esta ruta a la ruta deseada

        # Escribir el contenido en un archivo CSV en la ruta especificada
        with open(ruta_archivo_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([contenido])
            
        print(f"El contenido se ha guardado en {ruta_archivo_csv}")
    else:
        print("No se encontró ningún elemento con el XPath proporcionado.")
else:
    print("La solicitud GET no fue exitosa. Código de estado:", response.status_code)
