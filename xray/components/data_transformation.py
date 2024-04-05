import os
import sys
import joblib
from typing import Tuple
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder
from xray.constants import *
from xray.exception import CustomException
from xray.logger import logging
from xray.cloud_storage.s3_operations import S3Operation
from xray.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from xray.entity.artifact_entity import DataIngestionArtifacts, DataTransformationArtifacts

class DataTransformation:
    def __init__(self, 
                 data_ingestion_artifacts: DataIngestionArtifacts,
                 data_transformation_config: DataTransformationConfig):
        self.data_ingestion_artifacts = data_ingestion_artifacts
        self.data_transformation_config = data_transformation_config

    def transforming_training_data(self):
        try:
            logging.info(
                "Entered the transforming_training_data method of Data transformation class"
            )

            train_transform = transforms.Compose(
                [
                    transforms.Resize(self.data_transformation_config.RESIZE),
                    transforms.CenterCrop(self.data_transformation_config.CENTERCROP),
                    transforms.ColorJitter(
                        **self.data_transformation_config.COLOR_JITTER_TRANSFORMS
                    ),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomRotation(
                        self.data_transformation_config.RANDOMROTATION
                    ),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transformation_config.NORMALIZE_TRANSFORMS
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_training_data method of Data transformation class"
            )

            return train_transform

        except Exception as e:
            raise CustomException(e, sys)
        
    def transforming_testing_data(self):
        logging.info(
            "Entered the transforming_testing_data method of Data transformation class"
        )

        try:
            test_transform = transforms.Compose(
                [
                    transforms.Resize(self.data_transformation_config.RESIZE),
                    transforms.CenterCrop(self.data_transformation_config.CENTERCROP),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transformation_config.NORMALIZE_TRANSFORMS
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_testing_data method of Data transformation class"
            )

            return test_transform

        except Exception as e:
            raise CustomException(e, sys)


    def data_loader(
            self, train_transform: transforms.Compose, test_transform: transforms.Compose
        ) -> Tuple[DataLoader, DataLoader]:
        try:
            logging.info("Entered the data_loader method of Data transformation class")

            train_data: Dataset = ImageFolder(
                os.path.join(self.data_ingestion_artifacts.train_file_path),
                transform=train_transform,
            )

            test_data: Dataset = ImageFolder(
                os.path.join(self.data_ingestion_artifacts.test_file_path),
                transform=test_transform,
            )

            logging.info("Created train data and test data paths")

            train_loader: DataLoader = DataLoader(
                train_data, **self.data_transformation_config.DATA_LOADER_PARAMS
            )

            test_loader: DataLoader = DataLoader(
                test_data, **self.data_transformation_config.DATA_LOADER_PARAMS
            )

            logging.info("Exited the data_loader method of Data transformation class")

            return train_loader, test_loader

        except Exception as e:
            raise CustomException(e, sys)
   
    def initiate_data_transformation(self):
        try:
            logging.info(
                "Entered the initiate_data_transformation method of Data transformation class"
            )

            train_transform = self.transforming_training_data()

            test_transform = self.transforming_testing_data()

            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR, exist_ok=True)

            train_loader, test_loader = self.data_loader(
                train_transform=train_transform, 
                test_transform=test_transform
            )

            joblib.dump(
                train_transform, self.data_transformation_config.TRAIN_TRANSFORMS_FILE_PATH
            )

            joblib.dump(
                test_transform, self.data_transformation_config.TEST_TRANSFORMS_FILE_PATH
            )

            data_transformation_artifact = DataTransformationArtifacts(
                transformed_train_object=train_loader,
                transformed_test_object=test_loader,
                train_transform_file_path=self.data_transformation_config.TRAIN_TRANSFORMS_FILE_PATH,
                test_transform_file_path=self.data_transformation_config.TEST_TRANSFORMS_FILE_PATH,
            )

            logging.info(
                "Exited the initiate_data_transformation method of Data transformation class"
            )

            return data_transformation_artifact
    
        except Exception as e:
            raise CustomException(e, sys)