import os
import sys

from xray.logger import logging
from xray.exception import CustomException


class S3Operation:
    def sync_folder_to_s3(self, folder: str, bucket_name: str, bucket_folder_name: str):
        try:
            logging.info("Syncing start to AWS S3")
            command = f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name}"

            os.system(command)
            logging.info("Syncing completed to AWS S3")

        except Exception as e:
            raise CustomException(e, sys)

    def sync_folder_from_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ):

        try:
            logging.info("Syncing start from AWS S3")
            command: str = (
                f"aws s3 sync s3://{bucket_name}/{bucket_folder_name}/ {folder} "
            )

            os.system(command)
            logging.info("Syncing completed from AWS S3")

        except Exception as e:
            raise CustomException(e, sys)
