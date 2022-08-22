import boto3
import io
from io import StringIO
from local_variable import AWS_REGION, endpoint_url


class S3Handler:
    def __init__(self) -> None:
        self.s3_client = boto3.client("s3", region_name=AWS_REGION, endpoint_url=endpoint_url)
        self.s3_resource = boto3.resource("s3", region_name=AWS_REGION, endpoint_url=endpoint_url)

    def create_bucket(self, bucket):
        location = {'LocationConstraint': AWS_REGION}
        return self.s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)

    def cleanup_s3_bucket(self, bucket):
        s3_bucket = self.s3_resource.Bucket(bucket)
        # Deleting objects
        for s3_object in s3_bucket.objects.all():
            s3_object.delete()
        # Deleting objects versions if S3 versioning enabled
        for s3_object_ver in s3_bucket.object_versions.all():
            s3_object_ver.delete()
        print("S3 Bucket cleaned up")

    def delete_bucket(self, bucket):
        self.s3_client.delete_bucket(Bucket=bucket)
        print("Amazon S3 Bucket has been deleted")

    def get_list_of_buckets(self):
        response = self.s3_client.list_buckets()
        return list(map(lambda item: item['Name'], response['Buckets']))

    def upload_generated_file_object(self, bucket, object_name, file_name):
        with open(file_name, 'rb') as f:
            self.s3_client.upload_fileobj(f, bucket, object_name)
            print(f"Generated has been uploaded to '{bucket}'")
    
    def read_file_from_s3(self, bucket, name_of_file):
        s3_object = self.s3_resource.Object(bucket, name_of_file)

        with io.BytesIO() as f:
            s3_object.download_fileobj(f)
            f.seek(0)
            data = f.read()
            print(f"Read data in bucket '{bucket}', file '{name_of_file}'")
        
        return StringIO(str(data,'utf-8'))

    def create_s3_notification(self, bucket_name: str, func_name: str, aws_id: str = '000000000000'):
        response = self.s3_client.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration={
                "LambdaFunctionConfigurations": [
                    {
                        "Id": "s3eventtriggerslambda",
                        "LambdaFunctionArn": f"arn:aws:lambda:{AWS_REGION}:{aws_id}:function:{func_name}",
                        "Events": ["s3:ObjectCreated:*"]
                    }
                ]
            }
        )

        return response