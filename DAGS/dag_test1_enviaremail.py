from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
from airflow import DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
    dag_id='ian_test1',
    default_args=default_args,
    description='Correo Simple',
    schedule_interval='* * * * *',
    start_date=datetime(2022,8,1),
    tags=['ejemplo1'],
    catchup=False
    
) as dag:
    send_email_notification= EmailOperator(
        task_id="send_test_email",
        to= "irumiche@globokas.com",
        subject="Correo de prueba",
        html_content="<h2>Esto es un correo de prueba"   
    )

#mostrando cambio

#mostrando cambio2