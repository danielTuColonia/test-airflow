import pandas as pd
import pickle
from sklearn.metrics import classification_report

def evaluate_model(**kwargs):
    # Cargar la ruta del modelo desde XCom
    model_path = kwargs['ti'].xcom_pull(key='best_model_path')
    
    # Deserializar el modelo desde el archivo pickle
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    
    # Cargar los datos de prueba desde XCom
    X_test_dict = kwargs['ti'].xcom_pull(key='X_test')
    y_test = kwargs['ti'].xcom_pull(key='y_test')
    X_test = pd.DataFrame.from_dict(X_test_dict)
    
    # Hacer predicciones
    y_pred = model.predict(X_test)
    
    # Evaluar el modelo
    report = classification_report(y_test, y_pred)
    print("Classification Report:\n", report)
