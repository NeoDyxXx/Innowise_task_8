from s3_handler import S3Handler
from dynamodb_handler import DynamoDBHandler
import pandas as pd


def lambda_handler(event, context):
    file_name = event['Records'][0]['body']
    s3_handler = S3Handler()
    dynamodb_handler = DynamoDBHandler()

    obj = s3_handler.s3_client.get_object(Bucket="innowise", Key=file_name)
    initial_df = pd.read_csv(obj['Body'])

    for index, item in initial_df.iterrows():
        dynamodb_handler.put_item_in_table('parse_data_type_one', {
            'file_name': file_name,
            'departure_name': item['departure_name'],
            'return': item['return']
        })