from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import sys
import os 

# Ajusta el path para que Airflow pueda encontrar las tareas en la carpeta `task`
dag_name = os.path.splitext(os.path.basename(__file__))[0]  # 'example_dag'
tasks_path = f"{os.getcwd()}/task/{dag_name}/"
sys.path.append(tasks_path)

# Importa las tareas desde la carpeta correspondiente
from task_1 import task_1_function
from task_2 import task_2_function

# Define el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    dag_name,
    default_args=default_args,
    description='Un DAG de ejemplo con tareas separadas en archivos .py',
    schedule_interval='@daily',
)

# Define las tareas del DAG utilizando las funciones importadas
task_1 = PythonOperator(
    task_id='task_1',
    python_callable=task_1_function,
    dag=dag,
)

task_2 = PythonOperator(
    task_id='task_2',
    python_callable=task_2_function,
    dag=dag,
)

# Establece dependencias entre las tareas
task_1 >> task_2
