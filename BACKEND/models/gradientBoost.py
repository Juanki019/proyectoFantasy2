class GradientBoost():
    def __init__(self):
        self.model = GradientBoostModel()

    def predict(self, data):
        return self.model.predict(data)
    
    self.gradient_boost_params = {
        'loss': ['squared_error'],   # Función de pérdida a optimizar (por ejemplo, 'ls' para mínimos cuadrados)
        'learning_rate': [0.01, 0.1, 0.2],  # Tasa de aprendizaje
        'n_estimators': [100, 200, 300],  # Número de estimadores
        'max_depth': [3, 5, 7],  # Profundidad máxima de cada árbol
        'min_samples_split': [2],  # Número mínimo de muestras requeridas para dividir un nodo interno
        'min_samples_leaf': [1],  # Número mínimo de muestras requeridas para estar en un nodo hoja
        'max_features': [None],  # Número de características a considerar al buscar la mejor división
        'random_state': [None]  # Semilla para controlar la aleatoriedad
    }

    def train_model_laliga_gradient(self):
        df = pd.read_csv(self.selected_data_source.get(), usecols=lambda x: x not in ['NOMBRE', 'EQUIPO', 'target'])
        selected_target = self.selected_target_variable.get()

        if selected_target not in df.columns:
            print(f"La columna '{selected_target}' no se encuentra en el DataFrame.")
            return

        X = df.drop(selected_target, axis=1)
        y = df[selected_target]

        imp = SimpleImputer(strategy='mean')
        X = imp.fit_transform(X)

        algorithm = self.selected_algorithm.get()
        if algorithm == 'GradientBoost':
            ModelClass = GradientBoostingRegressor()

            grid_search = GridSearchCV(estimator=ModelClass, param_grid=self.gradient_boost_params, cv=5, scoring='neg_mean_squared_error',
                                       n_jobs=-1)

            grid_search.fit(X, y)
            self.model = grid_search.best_estimator_
            # Crear una instancia del modelo de Gradient Boosting con los parámetros configurados
            #self.model = ModelClass(**self.gradient_boost_params).fit(X, y)

            # Usar validación cruzada en lugar de train_test_split
            cv_results = cross_validate(self.model, X, y, cv=10,
                                        scoring=('neg_mean_squared_error', 'neg_mean_absolute_error'))

            # Obtener las métricas promedio de la validación cruzada
            mse = -np.mean(cv_results['test_neg_mean_squared_error'])
            rmse = np.sqrt(mse)
            mae = -np.mean(cv_results['test_neg_mean_absolute_error'])
            self.result_text.set(f"MSE: {mse}, RMSE: {rmse}, MAE: {mae}")

            # Entrenar el modelo con todos los datos
            #self.model = ModelClass.fit(X, y)

            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            training_date = formatted_date

            algorithm_used = self.selected_algorithm.get()
            num_samples = len(X)

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

    def train_model_misterfantasy_gradient(self):

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

        algorithm = self.selected_algorithm.get()
        if algorithm == 'GradientBoost':
            ModelClass = GradientBoostingRegressor()

            grid_search = GridSearchCV(estimator=ModelClass, param_grid=self.gradient_boost_params, cv=5,
                                       scoring='neg_mean_squared_error',
                                       n_jobs=-1)

            grid_search.fit(X, y)
            self.model = grid_search.best_estimator_
            # Crear una instancia del modelo de Gradient Boosting con los parámetros configurados
            # self.model = ModelClass(**self.gradient_boost_params).fit(X, y)

            # Usar validación cruzada en lugar de train_test_split
            cv_results = cross_validate(self.model, X, y, cv=10,
                                        scoring=('neg_mean_squared_error', 'neg_mean_absolute_error'))

            # Obtener las métricas promedio de la validación cruzada
            mse = -np.mean(cv_results['test_neg_mean_squared_error'])
            rmse = np.sqrt(mse)
            mae = -np.mean(cv_results['test_neg_mean_absolute_error'])
            self.result_text.set(f"MSE: {mse}, RMSE: {rmse}, MAE: {mae}")

            # Entrenar el modelo con todos los datos
            #self.model = ModelClass().fit(X, y)

            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            training_date = formatted_date

            algorithm_used = self.selected_algorithm.get()
            num_samples = len(X)

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
