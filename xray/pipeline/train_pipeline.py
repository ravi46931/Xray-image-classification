import os
import sys
from xray.constants import *
from xray.exception import CustomException
from xray.logger import logging
from xray.components.data_ingestion import DataIngestion
from xray.components.data_transformation import DataTransformation
from xray.components.model_trainer import ModelTrainer
from xray.components.model_evaluation import ModelEvaluation
from xray.components.model_pusher import ModelPusher
from xray.entity.artifact_entity import DataIngestionArtifacts
from xray.entity.config_entity import (DataIngestionConfig,
                                       DataTransformationConfig,
                                       ModelTrainerConfig,
                                       ModelEvaluationConfig)

class TrainPipeline:
    def __init__ (self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()

    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion(
                self.data_ingestion_config
            )

            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

            return data_ingestion_artifacts
        
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self, data_ingestion_artifacts):
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifacts,
                self.data_transformation_config
            )

            data_transformation_artifacts = data_transformation.initiate_data_transformation()

            return data_transformation_artifacts
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifacts):
        try:
            model_trainer = ModelTrainer(
                data_transformation_artifacts,
                self.model_trainer_config
            )

            model_trainer_artifacts = model_trainer.initiate_model_trainer()

            return model_trainer_artifacts
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_evaluation(self, 
                               data_transformation_artifacts,
                               model_trainer_artifacts):
        try:
            model_evaluation = ModelEvaluation(
                data_transformation_artifacts,
                model_trainer_artifacts,
                self.model_evaluation_config
            )

            model_evaluation_artifacts = model_evaluation.initiate_model_evaluation()

            return model_evaluation_artifacts
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_pusher(self):
        try:
            model_pusher = ModelPusher()

            model_pusher.initiate_model_pusher()
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_transformation_artifacts = self.start_data_transformation(data_ingestion_artifacts)
            model_trainer_artifacts = self.start_model_trainer(data_transformation_artifacts)
            model_evaluation_artifacts = self.start_model_evaluation( 
                               data_transformation_artifacts,
                               model_trainer_artifacts,
                               )
            self.start_model_pusher()
            
        except Exception as e:
            raise CustomException(e, sys)
        

if __name__=="__main__":
    train_pipeline = TrainPipeline()
    train_pipeline.run_pipeline()