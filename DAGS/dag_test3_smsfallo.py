import os
import pandas as pd
from datetime import datetime,timedelta
from airflow.models import DAG
from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.operators.email import EmailOperator
from twilio.rest import Client
import subprocess

#Definimos las funciones a utilizar
def procesar_fecha(ti):
    dt = ti.xcom_pull(task_ids=['obtener_fecha'])
    if not dt:
        raise Exception('No hay valor de fecha')

    dt = str(dt[0]).split()
    return {
        'year': int(dt[-1]),
        'month': dt[1],
        'day': int(dt[2]),
        'time': dt[3],
        'day_of_week': dt[0]
    }

def enviar_mensaje():
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid ='AC80a5adbc535bad9c30b80a32a395f5d7'
    auth_token ='f56e6372b437ef75f7efc0d23a90ba3e'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Hola mundo",
                        from_='+12183069958',
                        to='+51993343179'
                    )

    print(message.sid)

def guardar_fecha(ti):
    dt_processed = ti.xcom_pull(task_ids=['procesar_fecha'])
    if not dt_processed:
        raise Exception('No hay valor de fecha procesada')

    df = pd.DataFrame(dt_processed)

    csv_path = Variable.get('first_dag_csv_path')
    if os.path.exists(csv_path):
        df_header = False
        df_mode = 'a'
    else:
        df_header = True
        df_mode = 'w'

    df.to_csv(csv_path, index=False, mode=df_mode, header=df_header)


with DAG(
    dag_id='ian_test3',
    default_args={
        'depends_on_past': False,
        'email': ['irumiche@globokas.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        'on_failure_callback': enviar_mensaje,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    schedule_interval='* * * * *',
    start_date=datetime(year=2022, month=8, day=1),
    catchup=False,
    tags=['ejemplo3'],
) as dag:

    # 1. Obtener fecha actual
    task_obtener_fecha = BashOperator(
        task_id='obtener_fecha',
        bash_command='date'
    )

    # 2. Procesar fecha actual
    task_procesar_fecha = PythonOperator(
        task_id='procesar_fecha',
        python_callable=procesar_fecha
    )

    # 3. Guardar fecha procesada
    task_guardar_fecha = PythonOperator(
        task_id='guardar_fecha',
        python_callable=guardar_fecha
    )

    task_obtener_fecha >> task_procesar_fecha >> task_guardar_fecha