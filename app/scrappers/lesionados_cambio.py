import pandas as pd

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\data\\lesionados.csv')

# Realizar el cambio en la columna "nombre equipo"
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

# Guardar el DataFrame modificado de nuevo como un archivo CSV
df.to_csv('C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\data\\lesionados2.csv', index=False)
