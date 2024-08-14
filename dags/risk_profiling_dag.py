from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

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

# Tarea para instalar dependencias
install_dependencies = BashOperator(
    task_id='install_dependencies',
    bash_command='pip install pandas scikit-learn boto3 matplotlib seaborn smtplib email numpy',
    dag=dag,
)

# Función para ejecutar la tarea de preprocesamiento
def run_preprocess_data(**kwargs):
    from task.risk_profiling_dag.preprocess_data import preprocess_data
    return preprocess_data(**kwargs)

# Función para ejecutar la tarea de ajuste de hiperparámetros
def run_hyperparameter_tuning(**kwargs):
    from task.risk_profiling_dag.hyperparameter_tuning import hyperparameter_tuning
    return hyperparameter_tuning(**kwargs)

# Función para ejecutar la tarea de entrenamiento del modelo
def run_train_model(**kwargs):
    from task.risk_profiling_dag.train_model import train_model
    return train_model(**kwargs)

# Función para ejecutar la tarea de evaluación del modelo
def run_evaluate_model(**kwargs):
    from task.risk_profiling_dag.evaluate_model import evaluate_model
    return evaluate_model(**kwargs)

# Función para ejecutar la tarea de generación de reportes
def run_generate_report(**kwargs):
    from task.risk_profiling_dag.generate_report import generate_report
    return generate_report(**kwargs)

# Definir las tareas del DAG utilizando el operador Python y las funciones definidas
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=run_preprocess_data,
    provide_context=True,
    dag=dag,
)

tune_task = PythonOperator(
    task_id='hyperparameter_tuning',
    python_callable=run_hyperparameter_tuning,
    provide_context=True,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=run_train_model,
    provide_context=True,
    dag=dag,
)

evaluate_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=run_evaluate_model,
    provide_context=True,
    dag=dag,
)

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=run_generate_report,
    provide_context=True,
    dag=dag,
)

# Establecer la secuencia de tareas
install_dependencies >> preprocess_task >> tune_task >> train_task >> evaluate_task >> report_task
