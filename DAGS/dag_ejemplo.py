
from ast import operator
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.models.baseoperator import chain,cross_downstream

default_args={
    'retry':5,
    'retry_delay':timedelta(minutes=5)
}

def _downloading_data(**kwargs):
    with open("/tmp/myfile.txt","w") as f:
        f.write("my_data")
with DAG(
    dag_id='simple_dag', 
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2019,1,1),
    catchup=True,
    max_active_runs=3,

) as dag:
        
        task_1=DummyOperator(
            task_id='task_1',
            
        ) 
        
        task_2=DummyOperator(
            task_id='task_2',
            retry=3,
            #este retry tiene mayor prioridad
        )

        downloading_data=PythonOperator(
            task_id="downloadin_data",
            python_callable=_downloading_data
            
        )

        waiting_for_data=FileSensor(
            task_id="esperar_por_data",
            fs_conn_id="fs_default",
            filepath="my_file.txt",
            #poke_interval=15 chequear cada 15 seg si esta el archivo 
        )

        processing_data=BashOperator (
            task_id="procesar_data",
            bash_command="exit 0",
        )

downloading_data>>[waiting_for_data,processing_data]

chain (downloading_data,waiting_for_data,processing_data)

#cuando queramos crear dependencia entre dos listas
cross_downstream([downloading_data,processing_data],[waiting_for_data,processing_data])
## se puede añadir cosascomoop_kwargs={"my_param":42}
##0 **kwargs en el DEF para imprimir toda la info y en el print
# ds en el def y en el print para imprimir dia que se ejecuto el dag
#No poner  2 tareas en el mismo operador, tenerlo separado para mejor control
#One operator, one task
#backfill es util para el resumer, con corridas que tuvieron error y queremos
#verlas ahora en el resumen, si esta falso solo las ultimas corridas se mostra
#mostrarán
#schedule_interval=None para dags manuales totalmente
#schedule_interval="@daily" usando terminacion de airflow
#schedule_interval="******" usando cron expresion
#schedule_interval=timedelta(hours=7) para casos donde el cron no ejecuta bien
#XCOM es para compartir informacion entre tareas


#en una funcion 
def _checking_data(ti):
    my_xcom=ti.xcom.pull(key="return_value",task_ids=["downloading_data"])
    print(my_xcom)

