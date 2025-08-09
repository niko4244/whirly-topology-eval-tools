import boto3
import os

class S3Storage:
    def __init__(self, bucket_name, region_name=None):
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3", region_name=region_name)

    def upload_file(self, local_path, s3_key):
        self.s3.upload_file(local_path, self.bucket_name, s3_key)
        return f"s3://{self.bucket_name}/{s3_key}"

    def download_file(self, s3_key, local_path):
        self.s3.download_file(self.bucket_name, s3_key, local_path)
        return local_path

    def file_exists(self, s3_key):
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except self.s3.exceptions.ClientError:
            return False