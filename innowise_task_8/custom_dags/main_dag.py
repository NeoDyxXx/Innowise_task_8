from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from innowise_task_8.custom_operators.check_object import CheckObjectInAWS
from innowise_task_8.custom_operators.upload_data_in_s3 import UploadDataInS3
from innowise_task_8.custom_operators.upload_parse_data_in_s3 import UploadParseDataInS3


default_args = {
    'owner': 'airflow',
    'retries': 1
}


with DAG(
    dag_id='Innowise_task_8',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['Innowise task'],
    max_active_runs=1
) as dag:
    check_object = CheckObjectInAWS(
        task_id='check_object'
    )

    upload_stage_data = UploadDataInS3(
        task_id='upload_stage_data',
        data_repository='/home/ndx/Innowise tasks/Innowise_task_8/airflow/dags/innowise_task_8/test_data',
        bucket_name='innowise'
    )

    upload_parse_data = UploadParseDataInS3(
        task_id='upload_parse_data',
        data_repository='/home/ndx/Innowise tasks/Innowise_task_8/airflow/dags/innowise_task_8/test_data',
        bucket_name='innowise'
    )

    check_object >> [upload_stage_data, upload_parse_data]