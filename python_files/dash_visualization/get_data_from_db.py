from s3_handler import S3Handler
from dynamodb_handler import DynamoDBHandler

class GetDataFromDB:
    def __init__(self) -> None:
        self.__s3_handler = S3Handler()
        self.__dynamodb_handler = DynamoDBHandler()

    def _get_stage_data(self):
        list_of_files = self.__s3_handler.get_list_of_files_in_bucket('innowise')
        # list_of_files = ['split_data_2016-05_stage0.csv']
        list_of_files = [item for item in list_of_files if 'stage' in item.split('_')[-1]]
        print(list_of_files)

        list_of_rows = []
        for file in list_of_files:
            result = self.__dynamodb_handler.query_item_in_table('stage_data', 'file_name', file, 'innowise')
            list_of_rows.extend(result)

        return list_of_rows

    def _get_parse_data_type_one(self):
        list_of_files = self.__s3_handler.get_list_of_files_in_bucket('innowise')
        # list_of_files = ['split_data_2016-05_stage0.csv']
        list_of_files = [item for item in list_of_files if 'parse-type-one' in item.split('_')[-1]]

        list_of_rows = []
        for file in list_of_files:
            result = self.__dynamodb_handler.query_item_in_table('parse_data_type_one', 'file_name', file, 'innowise')
            list_of_rows.extend(result)

        for item in list_of_rows:
            item['return'] = str(item['return'])

        return list_of_rows

    def _get_parse_data_type_two(self):
        list_of_files = self.__s3_handler.get_list_of_files_in_bucket('innowise')
        # list_of_files = ['split_data_2016-05_stage0.csv']
        list_of_files = [item for item in list_of_files if 'parse-type-two' in item.split('_')[-1]]

        list_of_rows = []
        for file in list_of_files:
            result = self.__dynamodb_handler.query_item_in_table('parse_data_type_two', 'file_name', file, 'innowise')
            list_of_rows.extend(result)
            
        for item in list_of_rows:
            item['return'] = str(item['return'])

        return list_of_rows