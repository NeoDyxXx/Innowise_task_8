import boto3

endpoint_url = "http://localhost:4566"

dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)

# table = dynamodb.create_table (
# TableName = 'Employees',
# KeySchema = [
#         {
#             'AttributeName': 'departure_name',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName':'departure_id',
#             "KeyType" : 'RANGE'
#         }
#         ],
# AttributeDefinitions = [
#     {
#         'AttributeName':'departure_id',
#         'AttributeType': 'N'
#     },
#     {
#         'AttributeName':'departure_name',
#         'AttributeType': 'S'
#     }],
# ProvisionedThroughput={
#     'ReadCapacityUnits':1,
#     'WriteCapacityUnits':1
# }
# )
# print(table)

table = dynamodb.Table('Employees')

response = table.put_item(
Item = { 
     'departure_id': 111,
     'departure_name': '123',
     'name': 'hello',
     'new_type': 123
       }
)
print(response)
print()
print()
print()
print()

response = table.get_item(
    Key={
        'departure_id': 111,
        'departure_name': '123'
    }
)
print(response['Item'])