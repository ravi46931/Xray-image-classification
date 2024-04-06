import torch
from typing import List


ARTIFACTS = "artifacts"

# Data ingestion constants
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"
TRAIN_DIR = "train"
TEST_DIR = "test"
BUCKET_NAME: str = "xraylungimage"
S3_DATA_FOLDER: str = "data"


# Data transformation constants
DATA_TRANSFORMATION_ARTIFACTS_DIR = "DataTransformationArtifacts"

## Data Transformation
CLASS_LABEL_1: str = "NORMAL"

CLASS_LABEL_2: str = "PNEUMONIA"

BRIGHTNESS: int = 0.10

CONTRAST: int = 0.1

SATURATION: int = 0.10

HUE: int = 0.1

RESIZE: int = 224

CENTERCROP: int = 224

RANDOMROTATION: int = 10

NORMALIZE_LIST_1: List[int] = [0.485, 0.456, 0.406]

NORMALIZE_LIST_2: List[int] = [0.229, 0.224, 0.225]

TRAIN_TRANSFORMS_KEY: str = "xray_train_transforms"

TRAIN_TRANSFORMS_FILE: str = "train_transforms.pkl"

TEST_TRANSFORMS_FILE: str = "test_transforms.pkl"

BATCH_SIZE: int = 2

SHUFFLE: bool = False

PIN_MEMORY: bool = True


# Model Training Constants
TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_ARTIFACTS_DIR = "ModelTrainerArtifacts"
TRAINED_MODEL_NAME: str = "model.pt"
DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LEARNING_RATE = 0.01
MOMENTUM = 0.8
STEP_SIZE: int = 6
GAMMA: int = 0.5
EPOCHS: int = 100

# Model Evaluation Constants
MODEL_EVALUATION_ARTIFACTS_DIR = "ModelEvaluationArtifacts"
ACCURACY_FILE = "accuracy.json"

# Prediction constants
TARGET_WIDTH = 180
IMAGE_HEIGHT = 100
