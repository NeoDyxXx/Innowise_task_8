from s3_handler import S3Handler
from sqs_handler import SQSHandler
from parse_handler import ParseHandler


def lambda_handler(event, context):
    s3_client = S3Handler()
    parse_handle = ParseHandler('test1')

    if 'test1' not in s3_client.get_list_of_buckets():
        s3_client.create_bucket('test1')
    else:
        s3_client.cleanup_s3_bucket('test1')
        s3_client.delete_bucket('test1')
        s3_client.create_bucket('test1')

    s3_client.upload_generated_file_object('test1', 'data.csv', '/home/ndx/Innowise tasks/Innowise_task_8/python_files/split_data_2016-05.csv')
    print(parse_handle('data.csv'))


lambda_handler(None, None)