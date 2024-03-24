import pandas as pd

from app.querys.querys import cargar_datos_lesionados_en_bd


df = pd.read_csv('.../data/lesionados.csv')


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
csv_lesionados = df.to_csv('.../data/lesionados2.csv', index=False)

cargar_datos_lesionados_en_bd(csv_lesionados)