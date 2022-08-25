import logging
import boto3
from botocore.exceptions import ClientError


AWS_REGION = 'eu-west-1'
endpoint_url = "http://localstack:4566"

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

sqs_client = boto3.client("sqs", region_name=AWS_REGION, endpoint_url=endpoint_url)


def get_queue(queue_name):
    """
    Returns the URL of an existing Amazon SQS queue.
    """
    try:
        response = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']

    except ClientError:
        logger.exception(f'Could not get the {queue_name} queue.')
        raise
    else:
        return response


def send_queue_message(queue_url, msg_attributes, msg_body):
    """
    Sends a message to the specified queue.
    """
    try:
        response = sqs_client.send_message(QueueUrl=queue_url,
                                           MessageAttributes=msg_attributes,
                                           MessageBody=msg_body)
    except ClientError:
        logger.exception(f'Could not send meessage to the - {queue_url}.')
        raise
    else:
        return response


def lambda_handler(event, context): 
    file_name = event['Records'][0]['s3']['object']['key']

    if 'parse-type-one' in file_name.split('_')[-1]:
        send_queue_message(queue_url=get_queue('parse-files-queue-type-one'), msg_attributes={}, msg_body=file_name)
    elif 'parse-type-two' in file_name.split('_')[-1]:
        send_queue_message(queue_url=get_queue('parse-files-queue-type-two'), msg_attributes={}, msg_body=file_name)
    else:
        send_queue_message(queue_url=get_queue('stage-files-queue'), msg_attributes={}, msg_body=file_name)
        send_queue_message(queue_url=get_queue('metrics-queue'), msg_attributes={}, msg_body=file_name)

    logger.info(f'''
        Message sent to the queue.
        Message attributes: {file_name}''')

    return {"status_code": 200}