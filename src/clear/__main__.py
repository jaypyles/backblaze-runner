import os
from typing import Any

import boto3
import yaml
from botocore.exceptions import NoCredentialsError

from b2sdk.v1 import B2Api, InMemoryAccountInfo

key_id = ""
application_key = ""
info = InMemoryAccountInfo()

b2_api = B2Api(info)

b2_api.authorize_account("production", key_id, application_key)


def read_yaml() -> dict[str, Any]:
    with open("config.yaml") as f:
        y: dict[str, Any] = yaml.safe_load(f)
        return y


def upload_folder_to_s3(folder_path: str, bucket_name: str, s3_folder: str = ""):
    s3 = boto3.client("s3")
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Define the S3 key (the path within the S3 bucket)
            s3_key = os.path.join(
                s3_folder, os.path.relpath(file_path, folder_path)
            ).replace("\\", "/")

            try:
                # Upload each file to S3
                print(f"Uploading {file_path} to s3://{bucket_name}/{s3_key}")
                s3.upload_file(file_path, bucket_name, s3_key)
            except FileNotFoundError:
                print(f"The file {file_path} was not found.")
            except NoCredentialsError:
                print("AWS credentials not available.")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    folder_to_backup = "/path/to/your/local/folder"
    s3_bucket = "your-s3-bucket-name"
    s3_backup_folder = "backups/folder"
    upload_folder_to_s3(folder_to_backup, s3_bucket, s3_backup_folder)
