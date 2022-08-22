from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from innowise_task_8.custom_operators.check_object import CheckObjectInAWS

default_args = {
    'owner': 'airflow',
    'retries': 1
}


with DAG(
    dag_id='Innowise_task_6',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['Innowise task'],
    max_active_runs=1
) as dag:
    check_object = CheckObjectInAWS(
        task_id='check_object'
    )