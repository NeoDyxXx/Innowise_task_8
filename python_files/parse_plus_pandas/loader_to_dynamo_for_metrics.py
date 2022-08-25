from s3_handler import S3Handler
from dynamodb_handler import DynamoDBHandler
import pandas as pd


def lambda_handler(event, context):
    file_name = event['Records'][0]['body']
    s3_handler = S3Handler()
    dynamodb_handler = DynamoDBHandler()

    obj = s3_handler.s3_client.get_object(Bucket="innowise", Key=file_name)
    initial_df = pd.read_csv(obj['Body'])
    initial_df['avg_distance'] = initial_df['distance (m)'].mean()
    initial_df['avg_duration'] = initial_df['duration (sec.)'].mean()
    initial_df['avg_speed'] = initial_df['avg_speed (km/h)'].mean()
    initial_df['avg_temperature'] = initial_df['Air temperature (degC)'].mean()
    metrics = initial_df.iloc[0][['avg_distance', 'avg_duration', 'avg_speed', 'avg_temperature']].astype('string')

    dynamodb_handler.put_item_in_table('metrics_for_stage_data', {
        'file_name': file_name,
        'departure_name': '-',
        'avg_distance': metrics['avg_distance'],
        'avg_duration': metrics['avg_duration'],
        'avg_speed': metrics['avg_speed'],
        'avg_temperature': metrics['avg_temperature']
    })