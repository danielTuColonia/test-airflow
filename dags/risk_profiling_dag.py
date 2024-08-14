from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Importar las funciones desde los archivos .py en la carpeta tasks
from task.risk_profiling_dag.preprocess_data import preprocess_data
from task.risk_profiling_dag.train_model import train_model
from task.risk_profiling_dag.evaluate_model import evaluate_model
from task.risk_profiling_dag.hyperparameter_tuning import hyperparameter_tuning
from task.risk_profiling_dag.generate_report import generate_report

# Definir los argumentos por defecto del DAG
default_args = {
    'owner': 'skandia-daniel.grass',
    'start_date': datetime(2024, 8, 14),
    'retries': 1,
}

# Crear el DAG
dag = DAG(
    'risk_profiling_dag',
    default_args=default_args,
    description='DAG para perfilamiento de riesgo de clientes usando Random Forest',
    schedule_interval=None,  # No se ejecuta de forma recurrente
    catchup=False,  # No ejecuta tareas anteriores
)

# Definir las tareas del DAG utilizando los operadores de Python y las funciones importadas
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    provide_context=True,
    dag=dag,
)

tune_task = PythonOperator(
    task_id='hyperparameter_tuning',
    python_callable=hyperparameter_tuning,
    provide_context=True,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    provide_context=True,
    dag=dag,
)

evaluate_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    provide_context=True,
    dag=dag,
)

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    provide_context=True,
    dag=dag,
)

# Establecer la secuencia de tareas
preprocess_task >> tune_task >> train_task >> evaluate_task >> report_task
