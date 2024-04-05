import os
from xray.constants import *
from dataclasses import dataclass
from torch import device

@dataclass
class DataIngestionConfig:
    BUCKET_NAME = BUCKET_NAME
    S3_DATA_FOLDER = S3_DATA_FOLDER

    DATA_INGESTION_ARTIFACTS_DIR = os.path.join(ARTIFACTS, DATA_INGESTION_ARTIFACTS_DIR)
    DATA_PATH = os.path.join(DATA_INGESTION_ARTIFACTS_DIR, S3_DATA_FOLDER)
    TRAIN_PATH = os.path.join(DATA_PATH, TRAIN_DIR)
    TEST_PATH = os.path.join(DATA_PATH, TEST_DIR)

@dataclass
class DataTransformationConfig:
    DATA_TRANSFORMATION_ARTIFACTS_DIR = os.path.join(ARTIFACTS, DATA_TRANSFORMATION_ARTIFACTS_DIR)
    TRAIN_TRANSFORMS_FILE_PATH = os.path.join(DATA_TRANSFORMATION_ARTIFACTS_DIR, TRAIN_TRANSFORMS_FILE)
    TEST_TRANSFORMS_FILE_PATH = os.path.join(DATA_TRANSFORMATION_ARTIFACTS_DIR, TEST_TRANSFORMS_FILE)
    COLOR_JITTER_TRANSFORMS = {
            "brightness": BRIGHTNESS,
            "contrast": CONTRAST,
            "saturation": SATURATION,
            "hue": HUE,
        }
    RESIZE: int = RESIZE

    CENTERCROP: int = CENTERCROP

    RANDOMROTATION: int = RANDOMROTATION

    NORMALIZE_TRANSFORMS = {
            "mean": NORMALIZE_LIST_1,
            "std": NORMALIZE_LIST_2,
        }
    
    DATA_LOADER_PARAMS = {
            "batch_size": BATCH_SIZE,
            "shuffle": SHUFFLE,
            "pin_memory": PIN_MEMORY,
        }
    
@dataclass
class ModelTrainerConfig:
    MODEL_TRAINER_ARTIFACTS_DIR = os.path.join(ARTIFACTS, MODEL_TRAINER_ARTIFACTS_DIR)
    MODEL_FILE_PATH = os.path.join(MODEL_TRAINER_ARTIFACTS_DIR, TRAINED_MODEL_NAME)
    TRAIN_TRANSFORMS_KEY: str = TRAIN_TRANSFORMS_KEY

    EPOCHS: int = EPOCHS

    OPTIMIZER_PARAMS = {"lr": LEARNING_RATE, "momentum": MOMENTUM}
    
    SCHEDULAR_PARAMS = {"step_size": STEP_SIZE, "gamma": GAMMA}

    DEVICE: device = DEVICE 


@dataclass
class ModelEvaluationConfig:
    MODEL_EVALUATION_ARTIFACTS_DIR = os.path.join(ARTIFACTS, MODEL_EVALUATION_ARTIFACTS_DIR)

    ACCURACY_FILE_PATH = os.path.join(MODEL_EVALUATION_ARTIFACTS_DIR, ACCURACY_FILE)

    DEVICE: device = DEVICE 

    TEST_LOSS: int = 0

    TEST_ACCURACY: int = 0 

    TOTAL: int = 0

    TOTAL_BATCH: int = 0

    OPTIMIZER_PARAMS = {"lr": LEARNING_RATE, "momentum": MOMENTUM}

