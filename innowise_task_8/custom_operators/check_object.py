from airflow.models.baseoperator import BaseOperator
from innowise_task_8.another_classes.lambda_handler import LambdaHandler
from innowise_task_8.another_classes.s3_handler import S3Handler
from innowise_task_8.another_classes.sqs_handler import SQSHandler
from innowise_task_8.another_classes.logger_handler import LoggerHandler

class CheckObjectInAWS(BaseOperator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lambda_handler = LambdaHandler()
        self.s3_handler = S3Handler()
        self.sqs_handler = SQSHandler()
        self.logger_handler = LoggerHandler()

    def execute(self, context):
        try:
            self.logger_handler.log_message(self.s3_handler.create_bucket('innowise'))
        except:
            self.logger_handler.log_error('Bucket innowise is created.')

        try:
            self.logger_handler.log_message(self.sqs_handler.create_queue('parse-files-queue', '0', '30'))
            self.logger_handler.log_message(self.sqs_handler.create_queue('stage-files-queue', '0', '30'))
        except:
            self.logger_handler.log_error('Queues are created.')

        try:
            self.logger_handler.log_message(self.lambda_handler.create_iam_role('lambda_executer'))
        except:
            self.logger_handler.log_error("Role's created.")

        try:
            self.logger_handler.log_message(self.lambda_handler.create_lambda(
                '/home/ndx/Innowise tasks/Innowise_task_8/python_files/s3-notification-script/s3-notification-script.zip',
                's3-notification-script.lambda_handler',
                's3-notification', 
                'lambda_executer'))

            self.logger_handler.log_message(self.lambda_handler.create_lambda(
                '/home/ndx/Innowise tasks/Innowise_task_8/python_files/s3-notification-script/s3-notification-script.zip',
                's3-notification-script.lambda_handler',
                'parser_and_loader', 
                'lambda_executer'))
        except:
            self.logger_handler.log_error('Lambdas are created.')

        try:
            self.logger_handler.log_message(self.s3_handler.create_s3_notification('innowise', 's3-notification'))
        except:
            self.logger_handler.log_error('Notification are created.')

        try:
            self.logger_handler.log_message(self.lambda_handler.create_event_source_mapping('parser_and_loader', 'sqs', 'stage-files-queue'))
        except:
            self.logger_handler.log_error('Event sourse mapping are created.')