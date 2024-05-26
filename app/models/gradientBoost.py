import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, cross_val_predict
from sklearn.impute import SimpleImputer
import mysql.connector
import pickle
import os
import numpy as np 
from querys.querys import cargar_datos_todos_los_jugadores, cargar_datos_jugador_por_nombre

class GradientBoostModel():
    def __init__(self):
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
        players_data = cargar_datos_todos_los_jugadores()
        df = pd.DataFrame(players_data)

        if target_column not in df.columns:
            return "Columna objetivo no encontrada."

        X = df.drop(columns=[target_column])
        y = df[target_column]

        imp = SimpleImputer(strategy='mean')
        X = pd.DataFrame(imp.fit_transform(X), columns=X.columns)

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

        player_data = cargar_datos_jugador_por_nombre(player_name)

        if not player_data:
            return "Datos del jugador no disponibles."

        #Preparar los datos para la predicción, excluyendo el target
        player_df = pd.DataFrame([player_data])

        if target_column not in player_df.columns:
            print(f"La columna '{target_column}' no se encuentra en los datos del jugador.")
            return f"La columna '{target_column}' no se encuentra en los datos del jugador."

        features_used_during_fit = ['Puntos', 'Precio', 'Media', 'Partidos', 'Minutos', 'Goles', 'Asistencias']  # ajusta según tus datos
        features_used_during_fit.remove(target_column)

        X = player_df.drop(columns=[target_column])

        #Hacer la predicción
        predicted_value = self.model.predict(X)

        if isinstance(predicted_value, np.ndarray):
            predicted_value = predicted_value.tolist()

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
            return True
        except FileNotFoundError:
            print("Archivo no encontrado:", self.model_path)
            return False

    def close_db_connection(self):
        self.cursor.close()
        self.db_connection.close()