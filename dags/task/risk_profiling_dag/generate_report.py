from airflow.operators.email_operator import EmailOperator

def generate_report(**kwargs):
    # Cargar el reporte de clasificación desde XCom
    report = kwargs['ti'].xcom_pull(key='classification_report')
    
    # Opcional: Puedes guardar el reporte en un archivo y luego enviarlo por correo
    with open('/tmp/classification_report.txt', 'w') as f:
        f.write(report)
    
    # Configurar el envío de correo
    email = EmailOperator(
        task_id='send_email',
        to='tu_email@example.com',
        subject='Reporte de Clasificación del Modelo',
        html_content='Por favor, encuentra adjunto el reporte de clasificación.',
        files=['/tmp/classification_report.txt'],
        dag=kwargs['dag']
    )
    email.execute(context=kwargs)
