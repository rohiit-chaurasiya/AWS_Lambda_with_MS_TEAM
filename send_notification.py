import json
import boto3
from boto3.s3.transfer import S3Transfer

 

class SendNotification:

    def __init__(self) -> None:
        config_file_path = "config.json"
        with open(config_file_path, "r") as config_file:
            config_data = json.load(config_file)

        self.AWS_ACCESS_KEY = config_data["AWS_ACCESS_KEY"]
        self.AWS_SECRET_KEY = config_data["AWS_SECRET_KEY"]
        self.bucket_name = config_data["bucket_name"]
        self.image_file_path = config_data["image_file_path"]



    def uploading_daily_report(self, msg, image_file_path):
        try:
            s3_client = boto3.client('s3', aws_access_key_id=self.AWS_ACCESS_KEY, aws_secret_access_key=self.AWS_SECRET_KEY)
            transfer = S3Transfer(s3_client)

            transfer.upload_file(
                self. bucket_name,
                image_file_path,
                msg,
                extra_args={
                    'ServerSideEncryption': 'AES256',
                    'ContentType': 'image/png',  
                    'ACL': 'public-read', 
                    'ContentDisposition': 'inline' 
                }
            )
            print("File uploaded successfully with public-read access granted.")
        except Exception as e:
            print(f"Exception occurred in uploading_daily_report(): {e}")

