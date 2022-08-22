from innowise_task_8.another_classes.s3_handler import S3Handler
from airflow.models.baseoperator import BaseOperator
import os
import pandas as pd

class UploadParseDataInS3(BaseOperator):
    def __init__(self, data_repository: str, bucket_name: str, **kwargs):
        super().__init__(**kwargs)
        self.s3_handler = S3Handler()
        self.data_repository = data_repository
        self.bucket_name = bucket_name

    def execute(self, context):
        cwd = os.getcwd()
        os.chdir(self.data_repository)

        list_files = [item for item in os.listdir() if item.split('.')[-1] == 'csv']
        list_files = [item for item in list_files if 'parse' not in item.split('.')[1]]

        try:
            index = max([int(item.split('parse')[1].split('.')[0]) for item in self.s3_handler.get_list_of_files_in_bucket('innowise') if 'parse' in item.split('_')[-1]]) + 1
        except:
            index = 0

        for file_name in list_files:
            data = pd.read_csv(file_name)
            print(data.columns)
            data1 = data.groupby('departure_name').count()[['return']].reset_index()
            data2 = data.groupby(['departure_name', 'return_name']).count()[['return']].reset_index()

            data1.to_csv(file_name.split('.')[0] + '.parse0.csv', index=False)
            data2.to_csv(file_name.split('.')[0] + '.parse1.csv', index=False)

            self.s3_handler.upload_generated_file_object(self.bucket_name, file_name.split('.')[0] + '_parse-type-one' + str(index) + '.csv', file_name.split('.')[0] + '.parse0.csv')
            index += 1
            self.s3_handler.upload_generated_file_object(self.bucket_name, file_name.split('.')[0] + '_parse-type-two' + str(index) + '.csv', file_name.split('.')[0] + '.parse1.csv')
            index += 1

        os.chdir(cwd)