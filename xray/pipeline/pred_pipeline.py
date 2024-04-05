import os
import sys
from xray.constants import *
from xray.exception import CustomException
from xray.logger import logging
import os
import torch
import numpy as np
from PIL import Image
import streamlit as st
from pathlib import Path
from torchvision.transforms import transforms
import torchvision.transforms.functional as TF
from xray.constants import *


class PredPipeline:
    def __init__ (self):
        pass
    def transform_image(self, image):
        try:
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
            return transformed_img
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def prediction (self, transformed_img):
        try:

            model = torch.load(Path("model/model.pt"))
            output = model(transformed_img)
            prediction = int(torch.max(output.data, 1)[1].numpy())

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