import requests
from bs4 import BeautifulSoup
import pandas as pd
import subprocess

url = 'https://www.jornadaperfecta.com/lesionados/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

lesionados_divs = soup.find_all('div', class_='lesionados')

data = []
for div in lesionados_divs:
    equipo = div.find('div', class_='lesionados-equipo-nombre').text.strip()
    for jugador_div in div.find_all('div', class_='lesionados-jugador'):
        jugador_nombre = jugador_div.find('div', class_='lesionados-jugador-nombre').a.text.strip()
        jugador_lesion = jugador_div.find('div', class_='lesionados-jugador-motivo').text.strip()
        
        # Busca el elemento span con la clase 'bold' dentro del div actual
        estimacion_element = jugador_div.find('div', class_='lesionados-jugador-nombre').find('span', class_='bold')
        
        # Verifica si se encontró el elemento estimacion_element y extrae su texto
        if estimacion_element:
            estimacion = estimacion_element.text.strip()
        else:
            estimacion = None
        
        data.append([equipo, jugador_nombre, jugador_lesion])

df = pd.DataFrame(data, columns=['Equipo', 'Jugador', 'Lesion'])

# Guardar el archivo CSV inicial
csv_file_path = '.../data/lesionados.csv''.../data/lesionados.csv'
df.to_csv(csv_file_path, index=False)

# Llamar al script de filtrado
subprocess.run(['python', '.../data/lesionados.csv', csv_file_path])
