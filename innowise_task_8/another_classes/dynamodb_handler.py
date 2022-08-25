import boto3
from innowise_task_8.another_classes.local_variable import AWS_REGION, endpoint_url


class DynamoDBHandler:
    def __init__(self) -> None:
        self.dynamodb_handler = boto3.resource('dynamodb', region_name=AWS_REGION, endpoint_url=endpoint_url)

    def create_table(self, table_name, key_schema, attribute, provisioned):
        table = self.dynamodb_handler.create_table(
            TableName = table_name,
            KeySchema = key_schema,
            AttributeDefinitions = attribute,
            ProvisionedThroughput = provisioned
        )

        return table

    def put_item_in_table(self, table_name: str, items: dict):
        return self.dynamodb_handler.Table(table_name).put_item(
            Item = items)