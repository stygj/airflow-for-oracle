import boto3
from airflow.models.variable import Variable


class S3Client:
    def __init__(self):
        self.s3_bucket=Variable.get("S3_BUCKET")
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=Variable.get("S3_ACCESS_KEY_ID"),
            aws_secret_access_key=Variable.get("S3_SECRET_KEY"),
            region_name="ap-northeast-2"
        )
        
    def upload_file(self, file_path, obj_path):
        self.s3_client.upload_file(
            file_path,
            self.s3_bucket,
            obj_path
        )
