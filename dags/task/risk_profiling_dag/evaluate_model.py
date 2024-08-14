import pandas as pd
from sklearn.metrics import classification_report

def evaluate_model(**kwargs):
    # Cargar el modelo y los datos de prueba
    model = kwargs['ti'].xcom_pull(key='model')
    X_test_dict = kwargs['ti'].xcom_pull(key='X_test')
    y_test = kwargs['ti'].xcom_pull(key='y_test')
    
    X_test = pd.DataFrame.from_dict(X_test_dict)
    
    # Hacer predicciones
    y_pred = model.predict(X_test)
    
    # Evaluar el modelo
    report = classification_report(y_test, y_pred)
    print("Classification Report:\n", report)
    
    # Guardar el reporte para la siguiente tarea
    kwargs['ti'].xcom_push(key='classification_report', value=report)
