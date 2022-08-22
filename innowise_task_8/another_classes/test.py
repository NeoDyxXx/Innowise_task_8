import boto3
from local_variable import AWS_REGION, endpoint_url
from logger_handler import LoggerHandler
from botocore.exceptions import ClientError

class SQSHandler:
    def __init__(self) -> None:
        self.sqs_client = boto3.client("sqs", region_name=AWS_REGION, endpoint_url=endpoint_url)
        self.sqs_resource = boto3.resource("sqs", region_name=AWS_REGION, endpoint_url=endpoint_url)
        self.logger = LoggerHandler()

    def create_queue(self, queue_name, delay_seconds, visiblity_timeout):
        """
        Create a standard SQS queue
        """
        try:
            response = self.sqs_client.create_queue(QueueName=queue_name,
                                                Attributes = {
                                                    'DelaySeconds': delay_seconds,
                                                    'VisibilityTimeout': visiblity_timeout
                                                })
        except ClientError:
            self.logger.log_error(f'Could not create SQS queue - {queue_name}.')
            raise
        else:
            return response

    def list_queues(self):
        """
        Creates an iterable of all Queue resources in the collection.
        """
        try:
            sqs_queues = []
            for queue in self.sqs_resource.queues.all():
                sqs_queues.append(queue.url)
        except ClientError:
            self.logger.log_error('Could not list queues.')
            raise
        else:
            return sqs_queues
    
    def get_queue(self, queue_name):
        """
        Returns the URL of an existing Amazon SQS queue.
        """
        try:
            response = self.sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
        except ClientError:
            self.logger.log_error(f'Could not get the {queue_name} queue.')
            raise
        else:
            return response
    
    def delete_queue(self, queue_name):
        """
        Deletes the queue specified by the QueueUrl.
        """
        try:
            response = self.sqs_client.delete_queue(QueueUrl=queue_name)
        except ClientError:
            self.logger.log_error(f'Could not delete the {queue_name} queue.')
            raise
        else:
            return response
    
    def send_queue_message(self, queue_url, msg_attributes, msg_body):
        """
        Sends a message to the specified queue.
        """
        try:
            response = self.sqs_client.send_message(QueueUrl=queue_url,
                                            MessageAttributes=msg_attributes,
                                            MessageBody=msg_body)
        except ClientError:
            self.logger.log_error(f'Could not send meessage to the - {queue_url}.')
            raise
        else:
            return response
    
    def receive_queue_message(self, queue_url):
        """
        Retrieves one or more messages (up to 10), from the specified queue.
        """
        try:
            response = self.sqs_client.receive_message(QueueUrl=queue_url)
        except ClientError:
            self.logger.log_error(
                f'Could not receive the message from the - {queue_url}.')
            raise
        else:
            return response


    def delete_queue_message(self, queue_url, receipt_handle):
        """
        Deletes the specified message from the specified queue.
        """
        try:
            response = self.sqs_client.delete_message(QueueUrl=queue_url,
                                                ReceiptHandle=receipt_handle)
        except ClientError:
            self.logger.log_error(
                f'Could not delete the meessage from the - {queue_url}.')
            raise
        else:
            return response

    def get_message_with_delete(self, queue_url):
        messages = self.receive_queue_message(queue_url)
        try:
            for msg in messages['Messages']:
                msg_body = msg['Body']
                receipt_handle = msg['ReceiptHandle']

                self.logger.log_message(f'The message body: {msg_body}')
                self.logger.log_message('Deleting message from the queue...')

                self.delete_queue_message(queue_url, receipt_handle)
                break
        except:
            return None
        
        return msg_body

sqs_handler = SQSHandler()

print(sqs_handler.get_message_with_delete(sqs_handler.get_queue('parse-files-queue')))