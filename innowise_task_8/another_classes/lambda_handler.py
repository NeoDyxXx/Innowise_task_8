import boto3
from innowise_task_8.another_classes.local_variable import AWS_REGION, endpoint_url
import json

class LambdaHandler:
    def __init__(self) -> None:
        self.iam_client = boto3.client('iam', region_name=AWS_REGION, endpoint_url=endpoint_url)
        self.lambda_client = boto3.client('lambda', region_name=AWS_REGION, endpoint_url=endpoint_url)

    def create_iam_role(self, role_name: str):
        role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        response = self.iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(role_policy),
        )

        return response

    def create_lambda(self, source_from_zip: str, handler: str, func_name: str, role_name: str):
        with open(source_from_zip, 'rb') as f:
            zipped_code = f.read()
        
        role = self.iam_client.get_role(RoleName=role_name)

        response = self.lambda_client.create_function(
            FunctionName=func_name,
            Runtime='python3.8',
            Role=role['Role']['Arn'],
            Handler=handler,
            Code=dict(ZipFile=zipped_code),
            Timeout=300, # Maximum allowable timeout

            Environment={
                'Variables': {
                    'Name': 'helloWorldLambda',
                    'Environment': 'prod'
                }
            },
        )

        return response
    
    def invoke_lambda(self, func_name: str):
        test_event = dict()

        response = self.lambda_client.invoke(
            FunctionName=func_name,
            Payload=json.dumps(test_event),
        )

        return response

    def delete_lambda(self, lambda_name: str):
        response = self.lambda_client.delete_function(
            FunctionName=lambda_name
        )

        return response

    def create_event_source_mapping(self, func_name: str, object_type: str, object_name: str, aws_id: str = '000000000000'):
        response = self.lambda_client.create_event_source_mapping(
            EventSourceArn=f'arn:aws:{object_type}:{AWS_REGION}:{aws_id}:{object_name}',
            FunctionName=func_name,
            Enabled=True,
            BatchSize=1,
            StartingPosition='LATEST'
        )

        return response

    def get_event_source_mapping(self, func_name: str, object_type: str, object_name: str, aws_id: str = '000000000000'):
        response = self.lambda_client.list_event_source_mappings(
            EventSourceArn=f'arn:aws:{object_type}:{AWS_REGION}:{aws_id}:{object_name}',
            FunctionName=func_name
        )

        return response