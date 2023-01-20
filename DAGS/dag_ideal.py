
from datetime import datetime,timedelta
from airflow.models import DAG
from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.operators.email import EmailOperator


#Definimos las funciones a utilizar
def Conexion_DataBase():
    global cadena
    from decouple import config
    
    # Es importante habilitar mi ip en las redes permitidas
    # Obtén los detalles de conexión desde la configuración de la instancia de Cloud SQL
    DB_USER=config("USER_POSTGRES_GCP")
    DB_PASSWORD=config("PASS_POSTGRES_GCP")
    DB_NAME="postgres"
    DB_PORT="5432"
    DB_HOST=config("URL_POSTGRES_GCP")
    cadena  = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print('La conexión está correcta')
    

def Subir_Archivo():
    from sqlalchemy import create_engine
    import pandas as pd
    engine= create_engine(cadena,echo=True)
    print('La conexión está correcta')
    data={'name': ['John', 'Mike', 'Emily'],
            'age': [25, 30, 35],
            'city': ['New York', 'Los Angeles', 'Chicago']}
    df = pd.DataFrame(data)
    df.to_sql("Iris", con=engine, if_exists="append", index=False)



with DAG(
    dag_id='ian_test_EsSalud',
    default_args={
        'owner': 'Ian',
        'depends_on_past': False,
        'email': ['ianrumichejuarez@gmail.com'],
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
        # 'on_failure_callback': some_other_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description='#texto',
    schedule_interval='* * * * *',
    start_date=datetime(year=2022, month=8, day=1),
    catchup=False,
    tags=['Ejemplo'],

    
) as dag:

    # 1. Procesar fecha actual
    task_Conexion_DataBase = PythonOperator(
        task_id='Conexion_DataBase',
        python_callable=Conexion_DataBase
    )

    # 2. Guardar fecha procesada
    task_Subir_Archivo = PythonOperator(
        task_id='Subir_Archivo',
        python_callable=Subir_Archivo
    )

    task_Conexion_DataBase >> task_Subir_Archivo
