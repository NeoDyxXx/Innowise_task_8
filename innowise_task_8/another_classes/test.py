import imp
import boto3
from local_variable import *

dynamodb_handler = boto3.resource('dynamodb', region_name=AWS_REGION, endpoint_url=endpoint_url)

table = dynamodb_handler.create_table(
            TableName = 'data',
            KeySchema = [
                {
                    'AttributeName': 'file_name',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'departure_name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'file_name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName':'departure_name',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput = {
                'ReadCapacityUnits' : 1,
                'WriteCapacityUnits' : 1
            }
                
        )

print(table)