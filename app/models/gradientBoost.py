import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, cross_val_predict
from sklearn.impute import SimpleImputer
import mysql.connector
import pickle
import os

class GradientBoostModel():
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vicente1234",
            database="dreamxi"
        )
        self.cursor = self.db_connection.cursor(dictionary=True)
        self.model = None
        self.model_directory = 'data/'
        if not os.path.exists(self.model_directory):
            os.makedirs(self.model_directory)
        self.model_path = os.path.join(self.model_directory, 'gradient_boost_model.pkl')
        self.gradient_boost_params = {
            'loss': 'squared_error',
            'learning_rate': 0.1,
            'n_estimators': 100,
            'max_depth': 3,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'max_features': None,
            'random_state': None
        }

    def load_all_players_data(self):
        query = "SELECT Puntos, Precio, Media, Partidos, Minutos, Goles, Asistencias FROM jugadores"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def train_model(self, target_column):
        players_data = self.load_all_players_data()
        df = pd.DataFrame(players_data)

        if target_column not in df.columns:
            return "Columna objetivo no encontrada."

        X = df.drop(columns=[target_column])
        y = df[target_column]

        imp = SimpleImputer(strategy='mean')
        X = imp.fit_transform(X)

        # Configuración de parámetros
        parameters = {
            'loss': 'squared_error',
            'learning_rate': 0.1,
            'n_estimators': 100,
            'max_depth': 3,
            'min_samples_split': 2,
            'min_samples_leaf': 1
        }
        model = GradientBoostingRegressor(**parameters)
        self.model = GridSearchCV(model, {'n_estimators': [100, 200, 300]}, cv=5)
        self.model.fit(X, y)
        self.save_model()

    def predict(self, player_name, target_column):
        if self.model is None:
            self.model = self.load_model()
        if self.model is None:
            return "Modelo no entrenado."

        query = f"SELECT puntos, precio, media, partidos, minutos, goles, asistencias FROM jugadores WHERE nombre = %s"
        self.cursor.execute(query, (player_name,))
        player_data = self.cursor.fetchone()

        if not player_data:
            return "Datos del jugador no disponibles."

        # Preparar los datos para la predicción, excluyendo el target
        player_df = pd.DataFrame([player_data])
        X = player_df.drop(columns=[target_column])

        # Hacer la predicción
        predicted_value = self.model.predict(X)
        return predicted_value
        
    def save_model(self):
        with open(self.model_path, 'wb') as file:
            pickle.dump(self.model, file)
        print("Modelo guardado en:", os.path.abspath(self.model_path))

    def load_model(self):
        try:
            with open(self.model_path, 'rb') as file:
                self.model = pickle.load(file)
            print("Modelo cargado desde:", self.model_path)
        except FileNotFoundError:
            print("Archivo no encontrado:", self.model_path)
            self.model = None

    def close_db_connection(self):
        self.cursor.close()
        self.db_connection.close()