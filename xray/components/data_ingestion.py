import sys

from xray.constants import *
from xray.logger import logging
from xray.exception import CustomException
from xray.cloud_storage.s3_operations import S3Operation
from xray.entity.config_entity import DataIngestionConfig
from xray.entity.artifact_entity import DataIngestionArtifacts


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.s3 = S3Operation()

    def get_data_from_s3(self):
        try:
            self.s3.sync_folder_from_s3(
                self.data_ingestion_config.DATA_PATH,
                self.data_ingestion_config.BUCKET_NAME,
                self.data_ingestion_config.S3_DATA_FOLDER,
            )
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("Initiating data ingestion")
            self.get_data_from_s3()

            data_ingestion_artifacts = DataIngestionArtifacts(
                self.data_ingestion_config.TRAIN_PATH,
                self.data_ingestion_config.TEST_PATH,
            )
            logging.info("Data igestion completed")

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys)
