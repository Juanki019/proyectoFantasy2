import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="dreamxi",
        port=35024
    )

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

# Step 1: Scrape the data
url = 'https://www.jornadaperfecta.com/lesionados/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

lesionados_divs = soup.find_all('div', class_='lesionados')

data = []
for div in lesionados_divs:
    equipo = div.find('div', class_='lesionados-equipo-nombre').text.strip()
    for jugador_div in div.find_all('div', class_='lesionados-jugador'):
        jugador_nombre_div = jugador_div.find('div', class_='lesionados-jugador-nombre')
        if jugador_nombre_div and jugador_nombre_div.a:
            jugador_nombre = jugador_nombre_div.a.text.strip()
        else:
            jugador_nombre = 'Desconocido'

        jugador_lesion_div = jugador_div.find('div', class_='lesionados-jugador-motivo')
        jugador_lesion = jugador_lesion_div.text.strip() if jugador_lesion_div else 'Desconocido'
        
        # Busca el elemento span con la clase 'bold' dentro del div actual
        estimacion_element = jugador_nombre_div.find('span', class_='bold') if jugador_nombre_div else None
        
        # Verifica si se encontró el elemento estimacion_element y extrae su texto
        if estimacion_element:
            estimacion = estimacion_element.text.strip()
        else:
            estimacion = None
        
        data.append([equipo, jugador_nombre, jugador_lesion])

df = pd.DataFrame(data, columns=['Equipo', 'Jugador', 'Lesion'])

# Step 2: Save the initial CSV
csv_file_path = 'lesionados.csv'
df.to_csv(csv_file_path, index=False)

# Step 3: Process and clean the data
df['Equipo'] = df['Equipo'].replace({
    'Alavés': 'Deportivo Alavés', 
    'Almería': 'UD Almería',
    'Athletic': 'Athletic Club',
    'Atlético': 'Atlético de Madrid',
    'Barcelona': 'FC Barcelona',
    'Betis': 'Real Betis',
    'Cádiz CF': 'Cádiz CF',
    'Celta': 'RC Celta',
    'Girona': 'Girona FC',
    'Granada': 'Granada CF',
    'Las Palmas': 'UD Las Palmas',
    'Mallorca': 'RCD Mallorca',
    'Osasuna': 'C.A. Osasuna',
    'Rayo Vallecano': 'Rayo Vallecano',
    'Real Madrid': 'Real Madrid',
    'Real Sociedad': 'Real Sociedad',
    'Sevilla': 'Sevilla FC',
    'Valencia': 'Valencia CF',
    'Villarreal': 'Villarreal CF'
}, regex=True)

# Save the cleaned CSV
csv_lesionados_path = 'lesionados2.csv'
df.to_csv(csv_lesionados_path, index=False)

# Step 4: Load the cleaned data into the database
resultado = cargar_datos_lesionados_en_bd(csv_lesionados_path)
print(resultado)
print("actualizado bbdd lesionados")

