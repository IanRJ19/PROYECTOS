import os
import pandas as pd
from datetime import datetime,timedelta
from airflow.models import DAG
from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.operators.email import EmailOperator
from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

#Llamando a SLACK

SLACK_CONN_ID = 'slack'
def task_fail_slack_alert(context):
    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
    slack_msg = """
            :red_circle: Task Failed.
            <@U03V2A01KB6>  
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *gsutil URI*: {gsutil_URI} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            exec_date=context.get('execution_date'),
            gsutil_URI="gs://swift-airflow-gs/airflow/logs/{0}/{1}/{2}/{3}.log".format(context.get('task_instance').dag_id, context.get('task_instance').task_id,context.get('task_instance').execution_date,context.get('task_instance').prev_attempted_tries)
            )
    failed_alert = SlackWebhookOperator(
        task_id='slack_test',
        http_conn_id='slack',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow')
    return failed_alert.execute(context=context)

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
    dag_id='ian_test5',
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
        'on_failure_callback': task_fail_slack_alert,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    schedule_interval='* * * * *',
    start_date=datetime(year=2022, month=8, day=1),
    catchup=False,
    tags=['ejemplo5'],
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