import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

def generate_report(**kwargs):
    # Cargar la ruta del modelo desde XCom
    model_path = kwargs['ti'].xcom_pull(key='model_path')
    
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

    # Crear gráfica de la matriz de confusión
    conf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=[0, 1], yticklabels=[0, 1])
    plt.title('Matriz de Confusión')
    plt.xlabel('Predicción')
    plt.ylabel('Real')
    
    # Guardar la gráfica en un objeto BytesIO
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)

    # Configuración del correo electrónico
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "no.reply.colonia@gmail.com"
    smtp_password = "zfvcqtgcezeupsnd"  # Cambia esto por la contraseña correcta

    recipient = "recipient@example.com"  # Cambia esto por la dirección de correo del destinatario
    subject = "Prueba Skandia -Reporte de Clasificación y Matriz de Confusión"
    body = f"""
    Hola,

    Adjunto encontrarás el reporte de clasificación y la matriz de confusión generada por el modelo.

    {report}

    Saludos,
    El equipo de análisis
    """

    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = subject

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar la gráfica
    image = MIMEImage(img_data.read())
    image.add_header('Content-Disposition', 'attachment; filename="confusion_matrix.png"')
    msg.attach(image)

    # Enviar el correo electrónico
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Habilitar la seguridad TLS
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient, msg.as_string())
        server.quit()
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
