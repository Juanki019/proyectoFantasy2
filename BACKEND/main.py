import pickle
import tkinter as tk
from tkinter import ttk, filedialog
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
import os
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

class FantasyPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DreamXI")
        self.df = None
        self.save_model_path = tk.StringVar()

        root.configure(bg="#f0f0f0")

        # Carga y escala el logo
        logo_path = "logo_dreamXI.png"  # Actualiza con la ruta de tu logo
        logo = Image.open(logo_path)
        logo = logo.resize((50, 50), Image.Resampling.LANCZOS)  # Ajusta el tamaño según sea necesario
        logo = ImageTk.PhotoImage(logo)

        self.root.iconphoto(False, logo)

        # Variables
        self.selected_data_source = tk.StringVar()
        self.selected_algorithm = tk.StringVar()
        self.selected_option = tk.IntVar()
        self.model = None

        self.algorithms = {'Linear Regression': LinearRegression, 'SVM': SVC, 'KNN': KNeighborsClassifier,
                           'GradientBoost': GradientBoostingRegressor, 'Neural Network': MLPRegressor}

        self.tabControl = ttk.Notebook(root)

        # Styles
        style = ttk.Style()
        style.configure("TButton", background="#4CAF50", foreground="white")
        style.configure("TEntry", background="white")
        style.configure("TText", background="white")
        style.map("TButton",
                  background=[('active', '!disabled', '#45a049')],
                  foreground=[('active', '!disabled', 'white')]
                  )
        style.configure("TMenubutton", background="black", foreground="white", font=('Helvetica', 10))

        # Crear el ttk.Style y definir colores personalizados
        style = ttk.Style()
        style.theme_create("colorful", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": "#71a6d9"},
                "map": {"background": [("selected", "#ff5733")]}
            }
        })
        style.theme_use("colorful")

        self.tabControl = ttk.Notebook(root)

        #####################################
        # Fase 1: Entrenamiento
        #####################################
        self.train_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.train_tab, text="Entrenamiento")
        self.tabControl.pack(expand=1, fill="both")

        tk.Label(self.train_tab, text="Seleccione Fuente de Datos (CSV):").grid(row=1, column=0, pady=5, sticky="e")
        self.data_source_entry = ttk.Entry(self.train_tab, textvariable=self.selected_data_source, width=40,
                                           style="TEntry")
        self.data_source_entry.grid(row=1, column=1, sticky="w")
        ttk.Button(self.train_tab, text="Buscar", command=self.browse_data_source, style="TButton").grid(row=1,
                                                                                                         column=2,
                                                                                                         sticky="w")
        tk.Label(self.train_tab, text="Seleccione Algoritmo:").grid(row=2, column=0, pady=5, sticky="e")
        self.algorithm_menu = tk.OptionMenu(self.train_tab, self.selected_algorithm, *self.algorithms.keys())
        self.algorithm_menu.grid(row=2, column=1, sticky="w")

        tk.Label(self.train_tab, text="Seleccione target:").grid(row=2, column=1, pady=5, sticky="e")
        self.selected_target_variable = tk.StringVar()
        self.target_variable_menu = tk.OptionMenu(self.train_tab, self.selected_target_variable, 'PJ', 'G', 'Media',
                                                  'Precio')
        self.target_variable_menu.grid(row=2, column=2, sticky="w")

        self.target_variable_menu["menu"].entryconfig(0, foreground='red')
        self.target_variable_menu["menu"].entryconfig(1, foreground='red')
        self.target_variable_menu["menu"].entryconfig(2, foreground='blue')
        self.target_variable_menu["menu"].entryconfig(3, foreground='blue')

        ttk.Button(self.train_tab, text="Entrenar Modelo", command=self.train_model, style="TButton").grid(row=4,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=10)

        tk.Label(self.train_tab, text="Guardar modelo en:").grid(row=3, column=0, pady=5, sticky="e")
        self.save_model_entry = ttk.Entry(self.train_tab, textvariable=self.save_model_path, width=40, style="TEntry")
        self.save_model_entry.grid(row=3, column=1, sticky="w")
        ttk.Button(self.train_tab, text="Seleccionar Carpeta", command=self.browse_save_model, style="TButton").grid(
            row=3,
            column=2,
            sticky="w")

        self.selected_target_variable.trace_add("write", self.change_option_color)

        leyenda_label_train1 = tk.Label(self.train_tab,
                                        text="Si quieres predecir variable en rojo carga (table_data.csv)", fg='red')
        leyenda_label_train1.grid(row=2, column=4, columnspan=7, sticky="nsew")

        leyenda_label_train2 = tk.Label(self.train_tab,
                                        text="Si quieres predecir variable en azul carga (misterfantasy.csv)",
                                        fg='blue')
        leyenda_label_train2.grid(row=3, column=4, columnspan=7, sticky="nsew")

        #Crear figura plot
        self.fig = Figure(figsize=(4, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        #Crear canvas y añadirlo a la tab de entrenamiento
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.train_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, sticky="nsew")

        #Crear figura para la curva de aprendizaje
        self.learning_curve_fig = Figure(figsize=(4, 4), dpi=100)
        self.learning_curve_ax = self.learning_curve_fig.add_subplot(111)

        #Crear canvas y añadirlo a la tab de entrenamiento
        self.learning_curve_canvas = FigureCanvasTkAgg(self.learning_curve_fig, master=self.train_tab)
        self.learning_curve_canvas.draw()
        self.learning_curve_canvas.get_tk_widget().grid(row=6, column=10, columnspan=2, sticky="nsew")

        #Datos Extra del entrenamieto
        self.training_date_label = ttk.Label(self.train_tab, text="Fecha de realización:")
        self.training_date_label.grid(row=8, column=0, pady=5, sticky="e")

        self.algorithm_used_label = ttk.Label(self.train_tab, text="Algoritmo utilizado:")
        self.algorithm_used_label.grid(row=9, column=0, pady=5, sticky="e")

        self.num_samples_label = ttk.Label(self.train_tab, text="Nº de ejemplares empleados:")
        self.num_samples_label.grid(row=10, column=0, pady=5, sticky="e")

        self.metrics_label = ttk.Label(self.train_tab, text="Métricas del modelo:")
        self.metrics_label.grid(row=11, column=0, pady=5, sticky="e")

        #Campo para mostrar resultados del mse...
        self.result_text = tk.StringVar()
        self.result_label = ttk.Label(self.train_tab, textvariable=self.result_text)
        self.result_label.grid(row=11, column=1, columnspan=2, pady=5)

        ############################################
        # Fase 2: Data
        ##########################################
        self.data_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.data_tab, text="Datos")

        #Responsive
        for i in range(12):
            self.data_tab.grid_rowconfigure(i, weight=1)
            self.data_tab.grid_columnconfigure(i, weight=1)

        self.datos_LaLiga()

        # Tabla para jugadores lesionados
        cols_table = ('Equipo', 'Lesion', 'Jugador')
        self.tree_table = ttk.Treeview(self.data_tab, columns=cols_table, show='headings')

        for col in cols_table:
            self.tree_table.heading(col, text=col)

        for col in cols_table:
            self.tree_table.column(col, width=250)  # You can adjust the width as needed

        self.tree_table.grid(row=6, column=0, columnspan=3, sticky="nsew")

        self.display_info_in_table_lesionados()

        ttk.Button(self.data_tab, text="Actualizar Lesionados", command=self.ejecutar_script_actualizacion_lesionados,
                   style="TButton").grid(row=6, column=3,
                                         sticky="w")

        tk.Label(self.data_tab, text="Espere unos segundos...", fg='red').grid(row=7, column=5, sticky="e")

        ttk.Separator(self.data_tab, orient="horizontal").grid(row=8, column=0, columnspan=7, sticky="ew", pady=10)

        # Crea un Separator antes de la tabla
        separator = ttk.Separator(self.data_tab, orient="horizontal")
        separator.grid(row=11, column=0, columnspan=7, sticky="ew")

        # Crea un widget Treeview con 3 columnas
        cols = ('Nombre', 'Equipo', 'Partidos', 'Precio', 'Puntos', 'Goles', 'Amarillas')
        self.tree = ttk.Treeview(self.data_tab, columns=cols, show='headings')

        # Configurar las etiquetas de las columnas
        for col in cols:
            self.tree.heading(col, text=col)

        file_path_2023 = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\temporada2023.csv"
        if os.path.exists(file_path_2023) and os.access(file_path_2023, os.R_OK):
            df_2023 = pd.read_csv(file_path_2023)
            df_2023 = df_2023.sort_values(by='Puntos', ascending=False)
            for index, row in df_2023.iterrows():
                amarillas = int(row['Amarillas'])

                if amarillas == 4 or amarillas == 8 or amarillas == 12:
                    self.tree.insert("", "end", values=(
                    row['Nombre'], row['Equipo'], row['Partidos'], row['Precio'], row['Puntos'], row['Goles'],
                    row['Amarillas']), tags=('amarillo',))
                else:
                    self.tree.insert("", "end", values=(
                    row['Nombre'], row['Equipo'], row['Partidos'], row['Precio'], row['Puntos'], row['Goles'],
                    row['Amarillas']))

        self.tree.tag_configure('amarillo', background='yellow')

        self.tree.grid(row=9, column=0, columnspan=7, sticky="nsew")

        leyenda_label = tk.Label(self.data_tab, text="(*) Jugadores en amarillo tienen peligro de sanción", fg='red')
        leyenda_label.grid(row=12, column=0, columnspan=7, sticky="nsew")

        ############################################
        # Fase 3: Prediccion
        ##########################################
        self.prediction_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.prediction_tab, text="Prediccion")

        tk.Label(self.prediction_tab, text="STATS JUGADOR EN CAMPO:").grid(row=1, column=0, pady=5, sticky="e")
        tk.Label(self.prediction_tab, text="Selecciona jugador:").grid(row=2, column=0, pady=5, sticky="e")
        self.file_path ="C:\\UEM - 3\\Proyecto 1\\appfantasy\\table_data.csv"
        df = pd.read_csv(self.file_path)
        player_names = df['NOMBRE'].unique().tolist()
        self.selected_player_predict = tk.StringVar()
        self.player_menu = tk.OptionMenu(self.prediction_tab, self.selected_player_predict, *player_names)
        self.player_menu.grid(row=2, column=1, sticky="w")

        self.selected_player_predict_info_label = ttk.Label(self.prediction_tab, text="")
        self.selected_player_predict_info_label.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(self.prediction_tab, text="Mostrar Información", command=self.display_player_info2).grid(row=4,
                                                                                                            column=0,
                                                                                                            columnspan=2,
                                                                                                            pady=10)

        ttk.Separator(self.data_tab, orient="vertical").grid(row=0, column=3, columnspan=7, sticky="ew", pady=10)

        tk.Label(self.prediction_tab, text="DATOS ECONOMICOS/PUNTOS:").grid(row=1, column=6, pady=5, sticky="e")
        ttk.Button(self.prediction_tab, text="Misterfantasy", command=self.jugadores_mister).grid(row=1,
                                                                                                  column=7,
                                                                                                  columnspan=3,
                                                                                                  pady=10)

        self.prediction_label = ttk.Label(self.prediction_tab, text="PREDICCION SOBRE JUGADOR/ES")
        self.prediction_label.grid(row=8, column=0, columnspan=3, sticky="nsew")

        ttk.Button(self.prediction_tab, text="Predecir Valor", command=self.predict_value, style="TButton").grid(row=9,
                                                                                                                 column=0,
                                                                                                                 pady=10)

    ######################################
    # FUNCIONES VARIAS
    #####################################

    def ejecutar_script_actualizacion_lesionados(self):
        try:
            script_path = "lesionadosScrap.py"

            subprocess.run(["python", script_path], check=True)

            print("Actualización exitosa.")
            messagebox.showinfo("Éxito", "Actualización con éxito.")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el script de actualización: {e}")
            messagebox.showwarning("Advertencia", "Problemas con la actualiazción de los lesionados.")

    def jugadores_mister(self):

        tk.Label(self.prediction_tab, text="Selecciona jugador:").grid(row=2, column=6, pady=5, sticky="e")
        self.file_path_misterfantasy = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\misterfantasy.csv"
        df_misterfantasy = pd.read_csv(self.file_path_misterfantasy)
        player_names = df_misterfantasy['Nombre'].unique().tolist()
        self.selected_player_predict = tk.StringVar()
        self.player_menu = tk.OptionMenu(self.prediction_tab, self.selected_player_predict, *player_names)
        self.player_menu.grid(row=2, column=7, sticky="w")

        self.selected_player_predict_info_label = ttk.Label(self.prediction_tab, text="")
        self.selected_player_predict_info_label.grid(row=5, column=8, columnspan=2, pady=10)

        ttk.Button(self.prediction_tab, text="Mostrar Información",
                   command=self.display_player_info_misterfantasy).grid(row=6,
                                                                        column=8,
                                                                        columnspan=2,
                                                                        pady=10)

    def predict_value(self):
        selected_player_name = self.selected_player_predict.get()

        if selected_player_name:
            # Verificar si el nombre está todo en mayúsculas
            if selected_player_name.isupper():
                player_data = self.get_player_data(selected_player_name)
            else:
                player_data = self.get_player_data_mister(selected_player_name)

            # Verificar si se cargó un modelo
            if self.model:
                predicted_value = self.model.predict(player_data)

                self.prediction_label["text"] = f"Predicción para {selected_player_name}: {predicted_value}"
            else:
                messagebox.showwarning("Advertencia", "Primero entrena un modelo antes de realizar predicciones.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona un jugador antes de realizar una predicción.")

    def get_player_data(self, player_name):
        file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\table_data.csv"
        dataframe = pd.read_csv(file_path, index_col=0)

        # Obtener los datos del jugador del DataFrame
        player_data = dataframe[dataframe['NOMBRE'] == player_name]

        print(dataframe.columns)

        relevant_columns = ['MJ', 'PPJ', 'PC', 'PPC', 'PT', 'PPT', 'PS', 'PPS', 'TA', 'TR', 'SA', 'G', 'PR', 'GPP',
                            'GE']
        player_data = player_data[relevant_columns]

        return player_data

    def get_player_data_mister(self, player_name):
        file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\misterfantasy.csv"
        dataframe = pd.read_csv(file_path)

        # Obtener los datos del jugador del DataFrame
        player_data = dataframe[dataframe['Nombre'] == player_name]

        print(dataframe.columns)

        relevant_columns = ['Puntos_Totales', 'Media', 'puntos_ultima_jornada', 'puntos_penultima_jornada',
                            'puntos_antepenultima_jornada']
        player_data = player_data[relevant_columns]

        return player_data

    def show_player_stats(self):
        selected_player_name = self.selected_player_predict.get()
        selected_dataframe = self.df_liga if self.selected_data_source.get() == 'table_data.csv' else self.df_misterfantasy

        if selected_player_name:

            player_data = self.get_player_data(selected_player_name, selected_dataframe)

            stats_text = f"Estadísticas para {selected_player_name}:\n{player_data.to_string(index=False)}"
            messagebox.showinfo("Estadísticas del Jugador", stats_text)
        else:
            messagebox.showwarning("Advertencia", "Selecciona un jugador para ver sus estadísticas.")

    def browse_save_model(self):
        save_path = filedialog.askdirectory()
        self.save_model_path.set(save_path)

    def browse_data_source(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.selected_data_source.set(file_path)
        self.df = pd.read_csv(file_path)

    def display_player_info(self):
        #Obtener nombre del jugador seleccionado
        self.file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\table_data.csv"
        self.df_liga = pd.read_csv(self.file_path)

        selected_player_name = self.selected_player.get()

        if selected_player_name and self.df_liga is not None:
            selected_player_data = self.df_liga[self.df_liga['NOMBRE'] == selected_player_name].iloc[0]

            player_info_text = f"Nombre: {selected_player_data['NOMBRE']}\nEquipo: {selected_player_data['EQUIPO']}\nMinutos Jugados: {selected_player_data['MJ']}\nPartidos Completados: {selected_player_data['PC']}\nPartidos Sustituido: {selected_player_data['PS']}\nTarjetas Amarillas: {selected_player_data['TA']}\nTarjetas Rojas: {selected_player_data['TR']}\nGoles: {selected_player_data['G']}\nGoles en propia: {selected_player_data['GPP']}"
            self.selected_player_info_label.config(text=player_info_text)
        else:
            print("No se ha seleccionado ningún jugador para mostrar información.")
            messagebox.showwarning("Advertencia", "Selecciona un jugador antes de mostrar la información.")

    def display_player_info2(self):

        self.file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\table_data.csv"
        self.df_liga = pd.read_csv(self.file_path)

        selected_player_name = self.selected_player_predict.get()

        if selected_player_name and self.df_liga is not None:
            selected_player_data = self.df_liga[self.df_liga['NOMBRE'] == selected_player_name].iloc[0]

            player_info_text = f"Nombre: {selected_player_data['NOMBRE']}\nEquipo: {selected_player_data['EQUIPO']}\nMinutos Jugados: {selected_player_data['MJ']}\nPartidos Completados: {selected_player_data['PC']}\nPartidos Sustituido: {selected_player_data['PS']}\nTarjetas Amarillas: {selected_player_data['TA']}\nTarjetas Rojas: {selected_player_data['TR']}\nGoles: {selected_player_data['G']}\nGoles en propia: {selected_player_data['GPP']}"
            self.selected_player_predict_info_label.config(text=player_info_text)
        else:
            print("No se ha seleccionado ningún jugador para mostrar información.")
            messagebox.showwarning("Advertencia", "Selecciona un jugador antes de mostrar la información.")

    def display_player_info_misterfantasy(self):

        self.file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\misterfantasy.csv"
        self.df_liga = pd.read_csv(self.file_path)

        selected_player_name = self.selected_player_predict.get()

        if selected_player_name and self.df_liga is not None:
            selected_player_data = self.df_liga[self.df_liga['Nombre'] == selected_player_name].iloc[0]

            player_info_text = f"Nombre: {selected_player_data['Nombre']}\nMedia: {selected_player_data['Media']}\nSubida_Bajada: {selected_player_data['Subida_Bajada']}\nPrecio: {selected_player_data['Precio']}\nPuntos Última Jornada: {selected_player_data['puntos_ultima_jornada']}\nPuntos Penúltima Jornada: {selected_player_data['puntos_penultima_jornada']}\nPuntos Antepenúltima Jornada: {selected_player_data['puntos_antepenultima_jornada']}"
            self.selected_player_predict_info_label.config(text=player_info_text)
        else:
            print("No se ha seleccionado ningún jugador para mostrar información.")

    def update_team_players(self):
        selected_team = self.selected_team.get()
        self.file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\table_data.csv"
        self.df_liga = pd.read_csv(self.file_path)
        allowed_teams = ["REAL BETIS", "DEPORTIVO ALAVES", "RAYO VALLECANO", "RCD MALLORCA", "SEVILLA FC", "UD ALMERIA",
                         "VILLARREAL CF", "REAL SOCIEDAD", "CA OSASUNA", "ATHLETIC CLUB", "VALENCIA CF",
                         "UD LAS PALMAS", "GRANADA CF", "GIRONA CF", "FC BARCELONA", "REAL MADRID", "GETAFE CF",
                         "ATLETICO DE MADRID", "CADIZ CF", "RC CELTA"]  # Lista de equipos permitidos

        if selected_team and self.df_liga is not None:
            team_players = self.df_liga[
                (self.df_liga['EQUIPO'] == selected_team) & (self.df_liga['EQUIPO'].isin(allowed_teams))]
            player_info_text = "Jugadores y Estadísticas:\n"
            for _, player_data in team_players.iterrows():
                player_info_text += f"Nombre: {player_data['NOMBRE']}, Minutos Jugados: {player_data['MJ']},  Partidos de titular: {player_data['PT']},  Partidos Suplente: {player_data['PS']}, Goles: {player_data['G']}\n"

            self.selected_player_team_info_label.config(text=player_info_text)
        else:
            print("No se ha seleccionado ningún jugador para mostrar información.")
            messagebox.showwarning("Advertencia", "Selecciona un Equipo antes de mostrar la información.")

    def train_model(self):
        selected_variable = self.selected_target_variable.get()

        if selected_variable in ['PJ', 'G']:
            self.train_model_laliga()
        elif selected_variable in ['Media', 'Precio']:
            self.train_model_misterfantasy()
        else:
            print("Opción no válida")
            messagebox.showwarning("Advertencia", "Por favor, selecciona un target.")

    def train_model_laliga(self):

        df = pd.read_csv(self.selected_data_source.get(), usecols=lambda x: x not in ['NOMBRE', 'EQUIPO', 'target'])
        selected_target = self.selected_target_variable.get()

        if selected_target not in df.columns:
            print(f"La columna '{selected_target}' no se encuentra en el DataFrame.")
            return

        X = df.drop(selected_target, axis=1)
        y = df[selected_target]

        imp = SimpleImputer(strategy='mean')
        X = imp.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        algorithm = self.selected_algorithm.get()
        if algorithm in self.algorithms:
            ModelClass = self.algorithms[algorithm]
            self.model = ModelClass().fit(X_train, y_train)

            # Calcula las métricas del modelo
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            self.result_text.set(f"MSE: {mse}, RMSE: {rmse}, MAE: {mae}")
            train_sizes, train_scores, test_scores = learning_curve(self.model, X, y, cv=5)

            self.ax.clear()
            self.ax.scatter(X_train[:, 0], y_train, label='Training Data')
            self.ax.plot(X_test, y_pred, label='Predicted Values', color='red', linewidth=2)
            self.ax.legend()
            self.ax.set_xlabel('Features')
            self.ax.set_ylabel('Target')

            self.learning_curve_ax.clear()
            self.learning_curve_ax.plot(train_sizes, np.mean(train_scores, axis=1), label='Entrenamiento')
            self.learning_curve_ax.plot(train_sizes, np.mean(test_scores, axis=1), label='Prueba')
            self.learning_curve_ax.set_xlabel('Tamaño del Conjunto de Datos de Entrenamiento')
            self.learning_curve_ax.set_ylabel('Precisión')
            self.learning_curve_ax.set_title('Curva de Aprendizaje')
            self.learning_curve_ax.legend()

            self.canvas.draw()
            self.learning_curve_canvas.draw()

            #Curva de aprendizaje
            train_sizes, train_scores, test_scores = learning_curve(self.model, X, y, cv=5)
            plt.figure()
            plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Entrenamiento')
            plt.plot(train_sizes, np.mean(test_scores, axis=1), label='Prueba')
            plt.xlabel('Tamaño del Conjunto de Datos de Entrenamiento')
            plt.ylabel('Precisión')
            plt.title('Curva de Aprendizaje')
            plt.legend()

            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            training_date = formatted_date

            algorithm_used = self.selected_algorithm.get()
            num_samples = len(X_train) if 'X_train' in locals() else 0

            # Actualizar etiquetas con la información calculada
            self.training_date_label["text"] = f"Fecha de realización: {training_date}"
            self.algorithm_used_label["text"] = f"Algoritmo utilizado: {algorithm_used}"
            self.num_samples_label["text"] = f"Nº de ejemplares empleados: {num_samples}"

            save_path = self.save_model_path.get()
            if save_path:
                model_filename = "modelado_laliga.pkl"
                model_path = os.path.join(save_path, model_filename)

                # Guardar el modelo
                with open(model_path, 'wb') as file:
                    pickle.dump(self.model, file)
                print(f"Modelo guardado en: {model_path}")
            else:
                print("La ruta de guardado no está seleccionada.")

        else:
            print(f"Algoritmo desconocido: {algorithm}")
            messagebox.showwarning("Advertencia", "Por favor, selecciona un algoritmo antes de entrenar el modelo.")

    def train_model_misterfantasy(self):

        df = pd.read_csv(self.selected_data_source.get(),
                         usecols=lambda x: x not in ['Nombre', 'Posicion', 'Subida_Bajada'])
        selected_target = self.selected_target_variable.get()

        if selected_target not in df.columns:
            print(f"La columna '{selected_target}' no se encuentra en el DataFrame.")
            return

        X = df.drop(selected_target, axis=1)
        y = df[selected_target]

        imp = SimpleImputer(strategy='mean')
        X = imp.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        algorithm = self.selected_algorithm.get()
        if algorithm in self.algorithms:
            ModelClass = self.algorithms[algorithm]
            self.model = ModelClass().fit(X_train, y_train)

            # Calcula las métricas del modelo
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            self.result_text.set(f"MSE: {mse}, RMSE: {rmse}, MAE: {mae}")
            train_sizes, train_scores, test_scores = learning_curve(self.model, X, y, cv=5)

            self.ax.clear()
            self.ax.scatter(X_train[:, 0], y_train, label='Training Data')
            self.ax.plot(X_test, y_pred, label='Predicted Values', color='red', linewidth=2)
            self.ax.legend()
            self.ax.set_xlabel('Features')
            self.ax.set_ylabel('Target')

            self.learning_curve_ax.clear()
            self.learning_curve_ax.plot(train_sizes, np.mean(train_scores, axis=1), label='Entrenamiento')
            self.learning_curve_ax.plot(train_sizes, np.mean(test_scores, axis=1), label='Prueba')
            self.learning_curve_ax.set_xlabel('Tamaño del Conjunto de Datos de Entrenamiento')
            self.learning_curve_ax.set_ylabel('Precisión')
            self.learning_curve_ax.set_title('Curva de Aprendizaje')
            self.learning_curve_ax.legend()

            # Dibuja el nuevo gráfico
            self.canvas.draw()
            self.learning_curve_canvas.draw()

            # Añade la curva de aprendizaje
            train_sizes, train_scores, test_scores = learning_curve(self.model, X, y, cv=5)
            plt.figure()  # Crea una nueva figura para la curva de aprendizaje
            plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Entrenamiento')
            plt.plot(train_sizes, np.mean(test_scores, axis=1), label='Prueba')
            plt.xlabel('Tamaño del Conjunto de Datos de Entrenamiento')
            plt.ylabel('Precisión')
            plt.title('Curva de Aprendizaje')
            plt.legend()

            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            training_date = formatted_date

            algorithm_used = self.selected_algorithm.get()
            num_samples = len(X_train) if 'X_train' in locals() else 0

            # Actualizar etiquetas con la información calculada
            self.training_date_label["text"] = f"Fecha de realización: {training_date}"
            self.algorithm_used_label["text"] = f"Algoritmo utilizado: {algorithm_used}"
            self.num_samples_label["text"] = f"Nº de ejemplares empleados: {num_samples}"

            save_path = self.save_model_path.get()
            if save_path:
                model_filename = "modelado_misterfantasy.pkl"
                model_path = os.path.join(save_path, model_filename)

                # Guardar el modelo
                with open(model_path, 'wb') as file:
                    pickle.dump(self.model, file)
                print(f"Modelo guardado en: {model_path}")
            else:
                print("La ruta de guardado no está seleccionada.")

        else:
            print(f"Algoritmo desconocido: {algorithm}")
            messagebox.showwarning("Advertencia", "Por favor, selecciona un algoritmo antes de entrenar el modelo.")

    def display_info_in_table_lesionados(self):
        # Load the injured players CSV here
        file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\lesionados.csv"
        self.df_injured = pd.read_csv(file_path)

        for item in self.tree_table.get_children():
            self.tree_table.delete(item)

        if self.df_injured is not None:
            for _, row in self.df_injured.iterrows():

                self.tree_table.insert("", "end", values=(row['Equipo'], row['Lesion'], row['Jugador']))
        else:
            print("No se ha cargado ningún archivo CSV de lesionados para mostrar información en la tabla.")

    def change_option_color(self, *args):
        selected_variable = self.selected_target_variable.get()

        if selected_variable == 'PJ':
            self.target_variable_menu.configure(fg='red')
        elif selected_variable == 'G':
            self.target_variable_menu.configure(fg='red')
        else:
            self.target_variable_menu.configure(fg='blue')

    def clear_player_info(self):
        self.selected_player_info_label.config(text="")

    def clear_team_info(self):
        self.selected_player_team_info_label.config(text="")

    def datos_LaLiga(self):

        tk.Label(
            self.data_tab,
            text="ESTADISTICAS EN CAMPO (by: LaLiga)",
            font=("Arial", 12),
        ).grid(row=0, column=0, pady=10, sticky="ew")

        # Lista de jugadores
        tk.Label(self.data_tab, text="Selecciona jugador:").grid(row=1, column=0, pady=5, sticky="e")
        self.file_path = "C:\\UEM - 3\\Proyecto 1\\appfantasy\\table_data.csv"
        if os.path.exists(self.file_path) and os.access(self.file_path, os.R_OK):
            df = pd.read_csv(self.file_path)
            player_names = df['NOMBRE'].unique().tolist()
            self.selected_player = tk.StringVar()

            self.player_menu = tk.OptionMenu(self.data_tab, self.selected_player, *player_names)
            self.player_menu.grid(row=1, column=1, sticky="w")

            self.selected_player_info_label = ttk.Label(self.data_tab, text="")
            self.selected_player_info_label.grid(row=2, column=0, columnspan=2, pady=10)

            ttk.Button(self.data_tab, text="Mostrar Información", command=self.display_player_info).grid(row=3,
                                                                                                         column=0,
                                                                                                         columnspan=2,
                                                                                                         pady=10)

        else:
            print("No se ha seleccionado ningún archivo CSV.")
            return

        self.browse_data_source()

        # Lista de equipos
        tk.Label(self.data_tab, text="Seleccionar Equipo:").grid(row=1, column=5, pady=5, sticky="e")
        self.selected_team = tk.StringVar()
        allowed_teams = ["REAL BETIS", "DEPORTIVO ALAVES", "RAYO VALLECANO", "RCD MALLORCA", "SEVILLA FC", "UD ALMERIA",
                         "VILLARREAL CF", "REAL SOCIEDAD", "CA OSASUNA", "ATHLETIC CLUB", "VALENCIA CF",
                         "UD LAS PALMAS", "GRANADA CF", "GIRONA CF", "FC BARCELONA", "REAL MADRID", "GETAFE CF",
                         "ATLETICO DE MADRID", "CADIZ CF", "RC CELTA"]
        teams = self.df['EQUIPO'].unique().tolist()
        teams = [team for team in teams if team in allowed_teams]
        self.team_menu = tk.OptionMenu(self.data_tab, self.selected_team, *teams)
        self.team_menu.grid(row=1, column=6, sticky="w")

        self.selected_player_team_info_label = ttk.Label(self.data_tab, text="")
        self.selected_player_team_info_label.grid(row=2, column=6, columnspan=2, pady=10)

        ttk.Button(self.data_tab, text="Mostrar Jugadores", command=self.update_team_players).grid(row=3,
                                                                                                   column=5,
                                                                                                   columnspan=2,
                                                                                                   pady=10)

        ttk.Separator(self.data_tab, orient="horizontal").grid(row=4, column=0, columnspan=7, sticky="ew", pady=10)

        ttk.Button(self.data_tab, text="Limpiar Jugador", command=self.clear_player_info).grid(row=6, column=4,
                                                                                               columnspan=2, pady=10)

        ttk.Button(self.data_tab, text="Limpiar Equipo", command=self.clear_team_info).grid(row=6, column=5,
                                                                                            columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FantasyPredictorApp(root)
    root.mainloop()



