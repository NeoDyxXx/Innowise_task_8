from s3_handler import S3Handler
from dynamodb_handler import DynamoDBHandler
import pandas as pd


def lambda_handler(event, context):
    file_name = event['Records'][0]['body']
    s3_handler = S3Handler()
    dynamodb_handler = DynamoDBHandler()

    obj = s3_handler.s3_client.get_object(Bucket="innowise", Key=file_name)
    initial_df = pd.read_csv(obj['Body'])
    initial_df = initial_df.astype('string').fillna('-')

    for index, item in initial_df.iterrows():
        dynamodb_handler.put_item_in_table('stage_data', {
            'file_name': file_name,
            'departure_name': item['departure_name'],
            'departure': item['departure'],
            'return': item['return'],
            'return_id': item['return_id'],
            'return_name': item['return_name'],
            'distance (m)': item['distance (m)'],
            'duration (sec.)': item['duration (sec.)'],
            'avg_speed (km/h)': item['avg_speed (km/h)'],
            'departure_latitude': item['departure_latitude'],
            'departure_longitude': item['departure_longitude'],
            'return_latitude': item['return_latitude'],
            'return_longitude': item['return_longitude'],
            'Air temperature (degC)': item['Air temperature (degC)']
        })