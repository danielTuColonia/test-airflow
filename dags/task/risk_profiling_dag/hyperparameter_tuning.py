import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

def hyperparameter_tuning(**kwargs):
    # Cargar los datos preprocesados
    data_dict = kwargs['ti'].xcom_pull(key='preprocessed_data')
    data = pd.DataFrame.from_dict(data_dict)
    
    # Separar las características y la variable objetivo
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Definir los parámetros para GridSearch
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [ 10, 20],
        'min_samples_split': [2],
        'min_samples_leaf': [2, 4]
    }
    
    # Configurar el modelo y GridSearchCV
    model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    
    # Imprimir mensaje antes de iniciar el ajuste de hiperparámetros
    print("Iniciando ajuste de hiperparámetros con GridSearchCV...")

    # Entrenar el modelo con búsqueda de hiperparámetros
    grid_search.fit(X_train, y_train)
    
    # Imprimir mensaje al finalizar el ajuste de hiperparámetros
    print("Ajuste de hiperparámetros completado.")
    print(f"Mejores parámetros encontrados: {grid_search.best_params_}")

    # Guardar el mejor modelo encontrado
    best_model = grid_search.best_estimator_
    kwargs['ti'].xcom_push(key='best_model', value=best_model)
