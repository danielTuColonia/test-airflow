import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_model(**kwargs):
    # Cargar los datos preprocesados
    data_dict = kwargs['ti'].xcom_pull(key='preprocessed_data')
    data = pd.DataFrame.from_dict(data_dict)
    
    # Separar las características y la variable objetivo
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenar el modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Guardar el modelo y los datos de prueba para la siguiente tarea
    kwargs['ti'].xcom_push(key='model', value=model)
    kwargs['ti'].xcom_push(key='X_test', value=X_test.to_dict())
    kwargs['ti'].xcom_push(key='y_test', value=y_test.to_list())
