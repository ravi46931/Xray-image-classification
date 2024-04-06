import sys
import torch
from pathlib import Path
from torchvision.transforms import transforms

from xray.constants import *
from xray.logger import logging
from xray.exception import CustomException


class PredPipeline:
    def __init__(self):
        pass

    def transform_image(self, image):
        try:
            logging.info(
                "Transforming the image to the model input format for prediction"
            )
            trans = transforms.Compose(
                [
                    transforms.RandomHorizontalFlip(),
                    transforms.Resize(RESIZE),
                    transforms.CenterCrop(CENTERCROP),
                    transforms.ToTensor(),
                ]
            )

            transformed_img = trans(image)
            grayscale_tensor = torch.mean(transformed_img, dim=0, keepdim=True)
            transformed_img = grayscale_tensor.repeat(1, 3, 1, 1)

            logging.info("Image transformed successfully for prediction")

            return transformed_img

        except Exception as e:
            raise CustomException(e, sys)

    def prediction(self, transformed_img):
        try:
            logging.info("Predicting the image")
            model = torch.load(Path("model/model.pt"))
            output = model(transformed_img)
            prediction = int(torch.max(output.data, 1)[1].numpy())

            logging.info("Prediction from the model successfully")

            if prediction == 0:
                return "Normal"
            elif prediction == 1:
                return "Pneumonia"

        except Exception as e:
            raise CustomException(e, sys)

    def run_prediction(self, image):
        try:
            transformed_img = self.transform_image(image)
            prediction = self.prediction(transformed_img)
            return prediction

        except Exception as e:
            raise CustomException(e, sys)

# Prediction pipeline