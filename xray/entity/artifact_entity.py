from dataclasses import dataclass
from torch.utils.data.dataloader import DataLoader

from xray.constants import *

@dataclass
class DataIngestionArtifacts:
    train_file_path: str
    test_file_path: str


@dataclass
class DataTransformationArtifacts:
    transformed_train_object: DataLoader
    transformed_test_object: DataLoader
    train_transform_file_path: str
    test_transform_file_path: str

@dataclass
class ModelTrainerArtifacts:
    model_path: str

@dataclass
class ModelEvaluationArtifacts:
    accuracy_path: str

