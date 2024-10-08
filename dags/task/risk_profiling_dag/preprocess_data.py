import pandas as pd
import boto3
from io import StringIO
from sklearn.preprocessing import LabelEncoder

def preprocess_data(**kwargs):
    # Parámetros del bucket y archivo
    bucket_name = 'tucolonia-bucket'
    file_key = 'data.csv'  # Nombre del archivo en el bucket S3

    # Leer el archivo CSV desde S3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    
    # Preprocesamiento básico (ajusta según sea necesario)
    data = data.dropna()  # Eliminar filas con valores nulos

    # Codificación de variables categóricas
    label_encoder = LabelEncoder()
    data['employment_status'] = label_encoder.fit_transform(data['employment_status'])
    
    # Guardar el resultado para las siguientes tareas
    kwargs['ti'].xcom_push(key='preprocessed_data', value=data.to_dict())

    print("DG-Skania:", data.columns)
