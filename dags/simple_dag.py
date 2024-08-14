from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

# Definir los argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Crear el DAG
dag = DAG(
    'simple_dag',
    default_args=default_args,
    description='Un DAG simple de ejemplo',
    schedule_interval='@daily',
)

# Crear una tarea Dummy
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# Crear otra tarea Dummy
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Establecer el flujo de las tareas
start >> end
