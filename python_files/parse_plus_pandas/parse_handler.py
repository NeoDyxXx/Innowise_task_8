from logger_handler import LoggerHandler
import pandas as pd
from s3_handler import S3Handler


class ParseHandler:
    def __init__(self, s3_bucket_name: str) -> None:
        self.s3_bucket_name = s3_bucket_name
        self.s3_client = S3Handler()
        self.logger = LoggerHandler()

    def __call__(self, file_name: str):
        data = pd.read_csv(self.s3_client.read_file_from_s3(self.s3_bucket_name, file_name))

        avg_distance = data['distance (m)'].mean()
        avg_duration = data['duration (sec.)'].mean()
        avg_speed = data['avg_speed (km/h)'].mean()
        avg_tempreture = data['Air temperature (degC)'].mean()
        self.logger.log_message(f"Parse metric in data from file '{file_name}'")

        return {
            'file_name': file_name,
            'avg_distance': avg_distance,
            'avg_duration': avg_duration,
            'avg_speed': avg_speed,
            'avg_tempreture': avg_tempreture
        }