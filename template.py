import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')
source_folder = 'xray'

list_of_files=[
    ".github/workflows/main.yml",
    f"{source_folder}/__init__.py",
    f"{source_folder}/components/__init__.py",
    f"{source_folder}/components/data_ingestion.py",
    f"{source_folder}/components/data_transformation.py",
    f"{source_folder}/components/model_trainer.py",
    f"{source_folder}/components/model_evaluation.py",
    f"{source_folder}/components/model_pusher.py",
    f"{source_folder}/cloud_storage/__init__.py",
    f"{source_folder}/cloud_storage/s3_operations.py",
    f"{source_folder}/cloud_storage/s3_ops.py",

    f"{source_folder}/utils/__init__.py",
    f"{source_folder}/utils/utils.py",
    f"{source_folder}/ml/__init__.py",
    f"{source_folder}/ml/arch.py",
    f"{source_folder}/ml/model_service.py",
    f"{source_folder}/ml/standardization.py",
    f"{source_folder}/constants/__init__.py",
    f"{source_folder}/pipeline/__init__.py",
    f"{source_folder}/pipeline/train_pipeline.py",
   
    f"{source_folder}/entity/__init__.py",
    f"{source_folder}/entity/config_entity.py",
    f"{source_folder}/entity/artifact_entity.py",
    f"{source_folder}/logger/__init__.py",
    f"{source_folder}/exception/__init__.py",
    "requirements.txt",
    "app.py",
    "train.py",
    "demo.py",
    "README.md",
    "setup.py",
    "Dockerfile",
    ".dockerignore",
    ".gitignore"
]

for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)
    print(os.path.split(filepath))

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        pass
            
