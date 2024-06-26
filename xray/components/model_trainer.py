import os
import sys
import torch
import joblib
from torch.nn import Module
import torch.nn.functional as F
from torch.optim import Optimizer
from torch.optim.lr_scheduler import StepLR, _LRScheduler
from tqdm import tqdm

from xray.constants import *
from xray.entity.artifact_entity import (
    DataTransformationArtifacts,
    ModelTrainerArtifacts,
)
from xray.entity.config_entity import ModelTrainerConfig
from xray.exception import CustomException
from xray.logger import logging
from xray.ml.arch import Net


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifacts: DataTransformationArtifacts,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config

        self.data_transformation_artifacts = data_transformation_artifacts

        self.model: Module = Net()

    def train(self, optimizer: Optimizer):

        try:
            logging.info("Entered the train method of Model trainer class")

            self.model.train()

            pbar = tqdm(self.data_transformation_artifacts.transformed_train_object)

            correct: int = 0

            processed = 0

            for batch_idx, (data, target) in enumerate(pbar):
                data, target = data.to(DEVICE), target.to(DEVICE)

                # Initialization of gradient
                optimizer.zero_grad()

                # In PyTorch, gradient is accumulated over backprop and even though thats used in RNN generally not used in CNN
                # or specific requirements
                ## prediction on data

                y_pred = self.model(data)

                # Calculating loss given the prediction
                loss = F.nll_loss(y_pred, target)

                # Backprop
                loss.backward()

                optimizer.step()

                # get the index of the log-probability corresponding to the max value
                pred = y_pred.argmax(dim=1, keepdim=True)

                correct += pred.eq(target.view_as(pred)).sum().item()

                processed += len(data)

                pbar.set_description(
                    desc=f"Loss={loss.item()} Batch_id={batch_idx} Accuracy={100*correct/processed:0.2f}"
                )

            logging.info("Exited the train method of Model trainer class")

        except Exception as e:
            raise CustomException(e, sys)

    def test(self):
        try:
            logging.info("Entered the test method of Model trainer class")

            self.model.eval()

            test_loss: float = 0.0

            correct: int = 0

            with torch.no_grad():
                for (
                    data,
                    target,
                ) in self.data_transformation_artifacts.transformed_test_object:
                    data, target = data.to(DEVICE), target.to(DEVICE)

                    output = self.model(data)

                    test_loss += F.nll_loss(output, target, reduction="sum").item()

                    pred = output.argmax(dim=1, keepdim=True)

                    correct += pred.eq(target.view_as(pred)).sum().item()

                test_loss /= len(
                    self.data_transformation_artifacts.transformed_test_object.dataset
                )

                print(
                    "Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n".format(
                        test_loss,
                        correct,
                        len(
                            self.data_transformation_artifacts.transformed_test_object.dataset
                        ),
                        100.0
                        * correct
                        / len(
                            self.data_transformation_artifacts.transformed_test_object.dataset
                        ),
                    )
                )

            logging.info(
                "Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)".format(
                    test_loss,
                    correct,
                    len(
                        self.data_transformation_artifacts.transformed_test_object.dataset
                    ),
                    100.0
                    * correct
                    / len(
                        self.data_transformation_artifacts.transformed_test_object.dataset
                    ),
                )
            )

            logging.info("Exited the test method of Model trainer class")

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        try:
            logging.info(
                "Entered the initiate_model_trainer method of Model trainer class"
            )

            model: Module = self.model.to(self.model_trainer_config.DEVICE)

            optimizer: Optimizer = torch.optim.SGD(
                model.parameters(), **self.model_trainer_config.OPTIMIZER_PARAMS
            )

            scheduler: _LRScheduler = StepLR(
                optimizer=optimizer, **self.model_trainer_config.SCHEDULAR_PARAMS
            )

            for epoch in range(1, self.model_trainer_config.EPOCHS + 1):
                print("Epoch : ", epoch)

                self.train(optimizer=optimizer)

                optimizer.step()

                scheduler.step()

                self.test()

            os.makedirs(
                self.model_trainer_config.MODEL_TRAINER_ARTIFACTS_DIR, exist_ok=True
            )

            torch.save(model, self.model_trainer_config.MODEL_FILE_PATH)

            os.makedirs("model", exist_ok=True)
            torch.save(model, f"model/{TRAINED_MODEL_NAME}")

            train_transforms_obj = joblib.load(
                self.data_transformation_artifacts.train_transform_file_path
            )

            model_trainer_artifact = ModelTrainerArtifacts(
                self.model_trainer_config.MODEL_FILE_PATH
            )

            logging.info(
                "Exited the initiate_model_trainer method of Model trainer class"
            )

            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)
