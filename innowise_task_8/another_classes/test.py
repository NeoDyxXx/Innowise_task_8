from lambda_handler import LambdaHandler
from s3_handler import S3Handler
from sqs_handler import SQSHandler

lambda_handler = LambdaHandler()
s3_handler = S3Handler()
sqs_handler = SQSHandler()

# print(init.create_iam_role('test-role'))
# print(init.create_lambda('/home/ndx/Innowise tasks/Innowise_task_8/python_files/s3-notification-script/s3-notification-script.zip',
#                          's3-notification-script.lambda_handler',
#                          'test-lambda', 'test-role'))
# print(init.invoke_lambda('test-lambda'))
# print(init.delete_lambda('test-lambda'))

# print(s3_handler.create_bucket('test-bucket'))
# print(lambda_handler.create_lambda('/home/ndx/Innowise tasks/Innowise_task_8/python_files/s3-notification-script/s3-notification-script.zip',
                        #  's3-notification-script.lambda_handler',
                        #  'test-lambda', 'test-role'))
# print(s3_handler.create_s3_notification('test-bucket', 'test-lambda'))
# print(sqs_handler.create_queue('parse-files-queue', '0', '30'))
# print(sqs_handler.create_queue('stage-files-queue', '0', '30'))

# print(lambda_handler.create_lambda('/home/ndx/Innowise tasks/Innowise_task_8/python_files/s3-notification-script/s3-notification-script.zip',
#                          's3-notification-script.lambda_handler',
#                          'test-lambda1', 'test-role'))
# print(lambda_handler.create_event_source_mapping('test-lambda1', 'sqs', 'stage-files-queue'))
# print(s3_handler.upload_generated_file_object('test-bucket', 'test-file4.csv', '/home/ndx/Innowise tasks/Innowise_task_8/split_data/split_data_2016-06.csv'))

# print(sqs_handler.get_message_with_delete(sqs_handler.get_queue('stage-files-queue')))