import os
import sys
import joblib
import json
from typing import Tuple

import torch
from xray.ml.arch import Net
from torch.nn import CrossEntropyLoss, Module
from torch.optim import SGD, Optimizer
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder
from xray.constants import *
from xray.exception import CustomException
from xray.logger import logging
from xray.cloud_storage.s3_operations import S3Operation
from xray.entity.config_entity import DataIngestionConfig, ModelEvaluationConfig
from xray.entity.artifact_entity import ModelTrainerArtifacts, DataTransformationArtifacts

class ModelEvaluation:
    def __init__ (self,
                   data_transformation_artifacts: DataTransformationArtifacts,
                   model_trainer_artifacts: ModelTrainerArtifacts,
                   model_evaluation_config: ModelEvaluationConfig
                   ):
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_artifacts = model_trainer_artifacts
        self.model_evaluation_config = model_evaluation_config

    def configuration(self) -> Tuple[DataLoader, Module, float, Optimizer]:
        logging.info("Entered the configuration method of Model evaluation class")

        try:
            test_dataloader: DataLoader = (
                self.data_transformation_artifacts.transformed_test_object
            )

            model: Module = Net()

            model: Module = torch.load(self.model_trainer_artifacts.model_path)

            model.to(self.model_evaluation_config.DEVICE)

            cost: Module = CrossEntropyLoss()

            optimizer: Optimizer = SGD(
                model.parameters(), **self.model_evaluation_config.OPTIMIZER_PARAMS
            )

            model.eval()

            logging.info("Exited the configuration method of Model evaluation class")

            return test_dataloader, model, cost, optimizer

        except Exception as e:
            raise CustomException(e, sys)
        

    def test_net(self) -> float:
        logging.info("Entered the test_net method of Model evaluation class")

        try:
            test_dataloader, net, cost, _ = self.configuration()

            with torch.no_grad():
                holder = []

                for _, data in enumerate(test_dataloader):
                    images = data[0].to(self.model_evaluation_config.DEVICE)

                    labels = data[1].to(self.model_evaluation_config.DEVICE)

                    output = net(images)

                    loss = cost(output, labels)

                    predictions = torch.argmax(output, 1)

                    for i in zip(images, labels, predictions):
                        h = list(i)

                        holder.append(h)

                    logging.info(
                        f"Actual_Labels : {labels}     Predictions : {predictions}     labels : {loss.item():.4f}"
                    )

                    self.model_evaluation_config.TEST_LOSS += loss.item()

                    self.model_evaluation_config.TEST_ACCURACY += (
                        (predictions == labels).sum().item()
                    )

                    self.model_evaluation_config.TOTAL_BATCH += 1

                    self.model_evaluation_config.TOTAL += labels.size(0)

                    logging.info(
                        f"Model  -->   Loss : {self.model_evaluation_config.TEST_LOSS/ self.model_evaluation_config.TOTAL_BATCH} Accuracy : {(self.model_evaluation_config.TEST_ACCURACY / self.model_evaluation_config.TOTAL) * 100} %"
                    )

            accuracy = (
                self.model_evaluation_config.TEST_ACCURACY
                / self.model_evaluation_config.TOTAL
            ) * 100

            accuracy_dict = {
                "ACCURACY ON TEST SET": accuracy
            }

            logging.info("Exited the test_net method of Model evaluation class")

            return accuracy_dict

        except Exception as e:
            raise CustomException(e, sys)
      

    def initiate_model_evaluation(self):
        try:
            accuracy = self.test_net()
            os.makedirs(self.model_evaluation_config.MODEL_EVALUATION_ARTIFACTS_DIR, exist_ok=True)

            with open(self.model_evaluation_config.ACCURACY_FILE_PATH, "w") as json_file:
                json.dump(accuracy, json_file)

            model_evaluation_artifacts = ModelTrainerArtifacts(
                self.model_evaluation_config.ACCURACY_FILE_PATH
            )

            return model_evaluation_artifacts
        
        
        except Exception as e:
            raise CustomException(e, sys)
        
    